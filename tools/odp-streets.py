import asyncio
import pathlib

import aiohttp
import pandas as pd

STREET_NAME_URL = (
    "https://data.austintexas.gov/api/views/kumu-nbtd/rows.csv?accessType=DOWNLOAD"
)
STREET_NAME_CSV = "austin-texas.csv"
OUTPUT_DIR = "odp-streets"


async def fetch(session, url):
    async with session.get(url) as response:
        return await response.text()


async def get_content(session, url, output):
    data = await fetch(session, url)
    output_dir = output.resolve().parent
    output_dir.mkdir(parents=True, exist_ok=True)
    output.write_text(data)


async def main():
    output_dir = pathlib.Path(OUTPUT_DIR)
    csv_file = output_dir / STREET_NAME_CSV

    # Retrieve the Austin street name database in CSV format.
    async with aiohttp.ClientSession() as session:
        await get_content(session, STREET_NAME_URL, csv_file)

    # CSV manipulations with Pandasself.
    pd_streets = pd.read_csv(csv_file.resolve())
    pd_streets.fillna("", inplace=True)

    # Prepare new DataFrame.
    df = pd.DataFrame(columns=["Street Name", "Mapper", "Reviewer"])
    df["Street Name"] = (
        pd_streets["PRE DIR"]
        + " "
        + pd_streets["STREET NAME"]
        + " "
        + pd_streets["STREET TYPE"]
        + " "
    )

    # Clean up.
    df.dropna(subset=["Street Name"], inplace=True)
    df["Street Name"] = df["Street Name"].str.strip()
    df = df[df["Street Name"].apply(lambda x: not str(x).isdigit())]

    # Re-index and sort the df.
    df.set_index("Street Name", inplace=True)
    df.sort_values("Street Name", inplace=True)

    # Save.
    df.to_csv(output_dir / "hackathon.csv")


if __name__ == "__main__":
    asyncio.run(main())
