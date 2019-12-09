import asyncio
import multiprocessing
import pathlib
import shlex
import subprocess
import sys

import aiohttp
from halo import Halo
import pandas as pd

CITY = "austin"
STATE = "texas"
CITY_NAME_STATE = f"{CITY}_{STATE}"
CITY_NAME_STATE_CSV = f"{CITY_NAME_STATE}-streets.csv"
CITY_NAME_STATE_FILTERED = f"{CITY_NAME_STATE}.filtered.osm"
CITY_NAME_STATE_OSM = f"{CITY_NAME_STATE}.osm"
CITY_NAME_STATE_POLY = f"{CITY_NAME_STATE}.poly"
CITY_NAME_STATE_POLY_URL = f"https://raw.githubusercontent.com/JamesChevalier/cities/master/united_states/{STATE}/{CITY_NAME_STATE_POLY}"
OSM_REGION = f"{STATE}-latest.osm.pbf"
OSM_REGION_URL = f"https://download.geofabrik.de/north-america/us/{OSM_REGION}"
OUTPUT_DIR = "osm-streets"
CHUNK_SIZE = 1024 * 2014


async def get_content(session, url, output):
    spinner = Halo(text=f"Downloading {url}")
    spinner.start()
    try:
        async with session.get(url) as response:
            output_dir = output.resolve().parent
            output_dir.mkdir(parents=True, exist_ok=True)
            with output.open(mode="wb") as fd:
                while True:
                    chunk = await response.content.read(CHUNK_SIZE)
                    if not chunk:
                        break
                    fd.write(chunk)
    except Exception as e:
        spinner.fail(f"{e}")
        sys.exit(1)
    else:
        spinner.succeed()


def execute(cmd, cwd=None, message="Loading"):
    spinner = Halo(text=message)
    spinner.start()
    try:
        subprocess.run(cmd, shell=True, check=True, capture_output=True, cwd=cwd)
    except subprocess.CalledProcessError as cpe:
        spinner.fail(
            f'"{cpe.cmd}" failed to execute with error code {cpe.returncode} for the following reason:\n'
            f"{cpe.stderr.decode('utf-8')}."
        )
        sys.exit(1)
    else:
        spinner.succeed()


async def main():
    output_dir = pathlib.Path(OUTPUT_DIR)

    # Retrieve the Texas state PBF file and the Austin Polygon.
    downloads = [
        (CITY_NAME_STATE_POLY_URL, output_dir / CITY_NAME_STATE_POLY),
        (OSM_REGION_URL, output_dir / OSM_REGION),
    ]
    async with aiohttp.ClientSession() as session:
        for download in downloads:
            url, output = download
            if not output.exists():
                await get_content(session, url, output)

    # Run osmosis to extract data within the boundaries of the Austin polygon.
    # Take 8-10 minutes to run.
    austin_osm = output_dir / CITY_NAME_STATE_OSM
    austin_poly = output_dir / CITY_NAME_STATE_POLY
    if not austin_osm.exists():
        workers = multiprocessing.cpu_count()
        osmosis_cmd = (
            f'osmosis --read-pbf-fast file="{OSM_REGION}" workers={workers} '
            f'--bounding-polygon file="{austin_poly.name}" '
            f'--write-xml file="{austin_osm.name}"'
        )
        execute(
            osmosis_cmd,
            cwd=output_dir,
            message=f'Processing "{OSM_REGION}" (takes 8-10 minutes)',
        )

    # Run osmfilter to limit the file content to the attributes we need.
    OSM_FILTERS = ["addr:street=", "addr:postcode="]
    austin_filtered = output_dir / CITY_NAME_STATE_FILTERED
    if not austin_filtered.exists():
        osmfilter_cmd = (
            f'osmfilter {austin_osm.name} --keep="{" or ".join(OSM_FILTERS)}" '
            f"--ignore-depedencies "
            f"--drop-relations "
            f"--drop-ways "
            f"-o={austin_filtered.name}"
        )
        execute(osmfilter_cmd, cwd=output_dir, message=f"Filtering {austin_osm.name}")

    # Run osmconvert to extract the information we need into a CSV file.
    austin_csv = output_dir / CITY_NAME_STATE_CSV
    if not austin_csv.exists():
        osmconvert_cmd = (
            f"osmconvert {austin_filtered.name} "
            f'--csv="{" ".join([f[:-1] for f in OSM_FILTERS])}" '
            "--csv-headline "
            "--csv-separator=, "
            f"-o={austin_csv.name}"
        )
        execute(osmconvert_cmd, cwd=output_dir, message=f"Saving data to {austin_csv}")

        # Clean up the result.
        pd_streets = pd.read_csv(austin_csv.resolve())
        df = pd.DataFrame(columns=["Street Name", "Zipcode"])
        df["Street Name"] = pd_streets["addr:street"]
        df["Zipcode"] = pd_streets["addr:postcode"]
        df.dropna(inplace=True)
        df.drop_duplicates(inplace=True)

        # sort the df.
        df.sort_values("Zipcode", inplace=True)

        # Save.
        df.to_csv(austin_csv)

        # Extras.
        valid = df["Zipcode"].str.isdigit()
        grouped = df[valid].groupby(["Zipcode"]).count()
        grouped.to_csv(output_dir / "austin-street-grouped.csv")


if __name__ == "__main__":
    asyncio.run(main())
