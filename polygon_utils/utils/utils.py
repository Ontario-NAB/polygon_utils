import json
import geojson
import logging
from shapely.geometry import shape, mapping, Polygon
from shapely.ops import cascaded_union

def load_polygon_from_file(file_path):
    """
    Helper function to read a geojson file and return the polygon stored within.
    """
    raw_data = json.loads(open(file_path).read())
    mp = geojson.loads(json.dumps(raw_data['geometries'][0]))
    Multipoly = shape(mp)
    return Multipoly

def write_polygon_to_file(polygon, file_path):
    """
    Helper function to take a polygon and write it to a file in geojson format.
    """
    gj = geojson.Feature(geometry=polygon, properties={})
    with open(file_path, 'w') as f:
        f.write(geojson.dumps(gj))

def fill_multipolygon(multipolygon, eps):
    """
    Helper function to take a multipolygon or polygon with holes and fill the holes to create a solid polygon.
    eps represents the amount of buffer space around each point (i.e. a larger eps results in less accuracy).
    """
    logging.info("Using eps: {}".format(eps))
    logging.info("Filling multipolygon.")
    omega = cascaded_union([
        Polygon(component.exterior).buffer(eps).buffer(-eps) for component in multipolygon
    ])
    return Polygon(list(zip(*omega.exterior.coords.xy)))

