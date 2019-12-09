# BNA hack-a-thon

## Goal

* One document (instead of 3)
* Less scrolling
* Simplify researching for examples and official pages
* Provide a way to monitor progress

## Setup

The tools require `Python 3.7+` and `invoke`.

```bash
brew install python3
pip3 install invoke
```

Then simply run `inv` to setup the environment.

## Images

Resize the images:

```bash
cd images-orig
mogrify -resize 240x -path ../images *.png
```

## Generate a list of Austin streets

### Street Names from the Open Data Portal of Austin

The city of Austin provides a full inventory of all the street names of the city:
* https://austintexas.gov/page/street-name-reservations
  * https://data.austintexas.gov/api/views/kumu-nbtd/rows.csv?accessType=DOWNLOAD

However not all the streets are mapped in OSM.

Use the `tools/odp-streets.py` script to generate the list.

### Polygon + map

Use the method described by [James Chevalier](https://github.com/JamesChevalier/cities) to generate the osm document
for Austin using [osmosis](https://wiki.openstreetmap.org/wiki/Osmosis)
([usage](https://wiki.openstreetmap.org/wiki/Osmosis/Detailed_Usage_0.47)).

Then use [osmfilter](https://wiki.openstreetmap.org/wiki/Osmfilter) and
[osmconvert](https://wiki.openstreetmap.org/wiki/Osmconvert) to extract the street information. See
[OSM help](https://help.openstreetmap.org/questions/9816/the-best-way-to-extract-street-list) for the detailed answer
which helped me generate the list of information needed.

Use the `tools/osm-streets.py` script to generate the list.
