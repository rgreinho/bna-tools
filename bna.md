# People For Bike - BNA Hack-a-thon

## Tags

For this exercise, here are the main tags we are focusing on:

* [cycleway](https://wiki.openstreetmap.org/wiki/Key:cycleway)
* [highway](https://wiki.openstreetmap.org/wiki/Key:highway)
* [lanes](https://wiki.openstreetmap.org/wiki/Key:lanes)
* [oneway](https://wiki.openstreetmap.org/wiki/Key:oneway)
* [maxspeed](https://wiki.openstreetmap.org/wiki/Key:maxspeed)
* [parking](https://wiki.openstreetmap.org/wiki/Key:parking:lane)
* [surface](https://wiki.openstreetmap.org/wiki/Key:surface)

## General explainations

### Side of the road

`left` and `right` are relative to the direction the line is drawn in OSM, which is indicated in OSM by an arrow on the
line, not necessarily the direction of travel on the bike lane.

In the examples bellow, `{side}` can be either `left`, `right`. When it is both, the direction is  omitted.

### Lanes

* Represent the count of car lanes.
* Center turn lanes must be included in the number of lanes.

## Bike facilities Examples

|Photo|Description|Tags|Note|
|---|---|---|---|
|![Trail or sidepath](images/trail-or-sidepath.png)|Trail or sidepath| highway=cycleway<br/>surface=asphalt|Must be drawn as its own centerline.|
|![Bike lane without parking](images/bike-lane-no-parking.png)|Bike lane without parking|cycleway:{side}=lane<br/>cycleway:{side}:width<br/>parking:lane:{side}=no_parking<br/>||
|![Bike lane with parking](images/bike-lane-with-parking.png)|Bike lane with parking|cycleway:{side}=lane<br/>cycleway:{side}:width<br/>parking:lane:{side}=parallel<br/>parking:lane:{side}:width||
|![Contraflow bike lane](images/contraflow-bike-lane.png)|Contraflow bike lane|oneway=yes<br/>cycleway:{side}=opposite_lane<br/>cycleway:{side}:width|
|![Bike + parking lane](images/bike+parking-lane.png)|Bike + parking lane|cycleway:{side}=lane<br/>cycleway:{side}:width<br/>parking:lane:{side}=parallel<br/>parking:lane:{side}:width|
|![Buffered bike lane](images/buffered-bike-lane.png)|Buffered bike lane|cycleway:{side}=buffered_lane<br/>cycleway:{side}:width||
|![One-way cycle track protected lane](images/one-way-cycle-track.png)|One-way cycle track<br/>Protected lane|cycleway:{side}=track|See also [cycle tracks alternative](#cycle-tracks-alternative)|
|![Contraflow Cycle track](images/contraflow-cycle-track.png)|Contraflow Cycle track|cycleway:{side}=opposite_track|
|![Two-way cycle track](images/two-way-cycle-track.png)|Two-way cycle track|highway=cycleway|Must be drawn as its own centerline.|
|![Sharows](images/sharrows.png)|Sharrows/Shared Lane|cycleway:{side}=shared_lane||

### Remarks

#### Lane width

Width values default to meters in OSM. To denote feet and inches, use the notation ‘ and “ respectively with no spaces
between. E.g. cycleway:right:width=3’10”

#### Cycleway width

Cycleway width should either be measured from any parking-related pavement markings (such as a T) to the edge line, or
as the leftover space after deducting eight feet for the parking. If both cycleway and parking widths are provided these
 should add up to the total width of the combined space.

#### Cycleway with buffer width

Cycleway width in this case should include the width of the lane and buffer combined.

#### Cycle tracks alternative

Cycle tracks can alternatively be mapped as a separate centerline, in which case they should be tagged as:

* highway=cycleway
* oneway=yes

## Resources

* [City of Austin - OSM Mapathon Instructions](https://github.com/cityofaustin/atd-geospatial/wiki/OSM-Mapathon-Instructions)
* [Bicycle Network Analysis OpenStreetMap Tag Guidelines](https://docs.google.com/document/d/1isc9M9_c-QL4Oy8_MxAyogZ6ocs1F6PeEn_Y1p0WZp8/edit#heading=h.zfgapbgr6a6l)
* [Mapping with OpenStreetMap](https://labs.mapbox.com/mapping/) (MapBox Mapping guides)
