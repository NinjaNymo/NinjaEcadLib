# KiCad Configuration
## Path Variables
In KiCad, go to _Preferences_ -> _Configure Paths..._ and add the following:

1. NINJALIB = C:\git\NinjaEcadLib\kicad\
2. NINJASTEP = C:\git\NinjaEcadLib\step\
3. NINJADATASHEET = _your datasheet folder_

Cange the paths to match where this repository is stored (C:\git in the above example).

## Symbol and Footprint Library Paths
With the path variables set up, first go to _Preferences_ -> _Manage Symbol Libraries..._ and add:

NinjaLib = ${NINJALIB}/ninjalib-sym-table

Then, go to _Preferences_ -> _Manage Footprint Libraries..._ and add:

NinjaLib = ${NINJALIB}/ninjalib-fp-table

### Creating New Libraries
The two table files (ninjalib-sym-table and ninjalib-fp-table) needs to be updated with new libraries such that KiCad can load them on boot.

## Datasheets
Datasheets are not stored in this repository for copyright reasons.

Instead, all symbols reference a path variable `{NINJADATASHEETS}` where the datasheets are expected to be stored.

### Datasheet Naming
Datasheets are stored with the following naming pattern:

_manufacturer_\__part-number_\__revision_\__publication-date_.pdf

* If the datasheet covers multiple part-numnbers, the part-family is used instead (typically the "title" of the datasheet).

* If revision is not provided, it is omitted.