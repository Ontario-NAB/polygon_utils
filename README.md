# Polygon Utils
This Python package contains some utility scripts to fill holes in polygons, union polygons, subtract polygons, and lookup points in a file containing several geojsons. The intended usage of this package is with OpenStreetMap geojson data. This package also contains an example data file (in the examples folder) which represents all the counties and districts in Ontario. Using the utility scripts in this package and geojson data from OSM, each county/district's polygon was created. This file is not meant to be a 100% accurate county map and should be used with discretion.

## Installation
To install this package, run:

    pip3 install ./

## Polygon Utils Usage
There are several scripts within the package, each with its own usage.

### Fill Multipolygon Usage
This script requires the path to a geojson containing a polygon/multipolygon with holes in it. The script will fill all holes in the polygon and write the resulting object to a geojson file.

-i, --infile: The path to the input (multi)polygon geojson.

-o, --outfile: The path to the output file.

-e, --eps: (Optional, default=0.0001) Value of the amount of buffer to use around each point. The higher the eps, the less accurate the resulting shape is.

Example usage:
    python3 ./polygon_utils/fill_multipolygon.py -i /path/to/input.json -o /path/to/output.json

### Symmetric Difference Multipolygon Usage
This script requires the path to two (multi)polygon geojsons, an outer (parent) and an inner (child). First any holes in these polygons are filled, and then a hole is created in the parent which corresponds to the child. The resulting shape is then written to the output file.

-p, --parent: The path to the input outer (multi)polygon geojson.

-c, --child: The path to the input inner (multi)polygon geojson.

-o, --outfile: The path to the output file.

-e, --eps: (Optional, default=0.0001) Value of the amount of buffer to use around each point. The higher the eps, the less accurate the resulting shape is.

Example usage:
    python3 ./polygon_utils/symmetric_difference_multipolygons.py -p /path/to/parent.json -c ../path/to/child.json -o /path/to/output.json

### Union Multipolygon Usage
This script takes in a semicolon-separated string of input geojsons. It first fills all the holes in any of the input polygons, and then attempts to union them. Only polygons which are adjacent (touching) may be unioned. The resulting object is then written to the output file.

-i, --infile: Semicolon-separated string of paths to the input (multi)polygon geojsons.

-o, --outfile: The path to the output file.

-e, --eps: (Optional, default=0.0001) Value of the amount of buffer to use around each point. The higher the eps, the less accurate the resulting shape is.

Example usage:
    python3 ./polygon_utils/union_multipolygons.py -i '/path/to/input1.json;/path/to/input2.json;/path/to/input3.json' -o /path/to/output.json

### Lookup Point Usage
This script takes the path to a special lookup input file which is a dictionary of geojsons (see Point Lookup Input File section below) and the x and y coordinate of a point. The script will check every feature defined in the input file to see if the point is contained within that feature. If a match is found, the key of that feature will be returned. Only the first match for a point is returned.

-i, --infile: The path to the file containing a dictionary of geojsons to search.

-x, --x: The x-coordinate of the Point to lookup.

-y --y: The y-coordinate of the Point to lookup.

Example usage:
    python3 ./polygon_utils/lookup_point.py -i /path/to/input.json -x 46.996439 -y -84.302183

## Point Lookup Input File
The input file for the Lookup Point script is a specially formatted json where the keys are the names of the features and the values are the geojsons representing those features. An example entry in this file is:
    {"FeatureA": {"type": "Feature", "geometry": {"type": "Polygon", "coordinates":[coords go here]}, "properties": {}}}
A full example of a proper input file for this script can be found in the 'examples' directory.