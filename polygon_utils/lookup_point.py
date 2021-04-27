import json
import logging
import argparse
from shapely.geometry import Point
from shapely.geometry import shape

def load_feature_map(infile):
    """
    Helper function to load a dictionary of geojsons into a new dictionary
    where the keys of the new dictionary are the same as the old and the values are
    the shapely representations of the geojsons.
    """
    logging.info('Loading feature map.')
    poly_dict = {}
    base_dict = json.load(open(infile))
    for key in base_dict:
        poly_dict[key] = shape(base_dict[key]['geometry'])
    return poly_dict

def lookup_point(poly_dict, point):
    """
    Helper function to search through poly_dict to see if point is contained within the shapes
    that are the values of poly_dict.
    If a match is found, the key is returned, if no match is found, an empty string is returned.
    Only the first match found is returned.
    """
    logging.info('Scanning feature map to check if point is contained in any feature')
    for key in poly_dict:
        if poly_dict[key].contains(point):
            logging.info('Point found in feature: {}'.format(key))
            return key
    logging.info('Point not present in any of the features in the map.')
    return ''

def lookup_point_wrapper(infile, x, y):
    """
    Wrapper function to encompass reading a dictionary of geojsons from a file,
    and checking whether the point represented by (x, y) is present within any of the shapes in the file.
    """
    poly_dict = load_feature_map(infile)
    point_to_lookup = Point(x, y)
    return lookup_point(poly_dict, point_to_lookup)

if __name__ == '__main__':
    logging.basicConfig(format='[%(asctime)s] %(levelname)s:%(message)s', level=logging.DEBUG)
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--infile', help='file path to the feature map file to lookup a point in')
    parser.add_argument('-x', '--x', help='x coordinate of the point to lookup', type=float)
    parser.add_argument('-y', '--y', help='y coordinate of the point to lookup', type=float)
    args = parser.parse_args()
    response = lookup_point_wrapper(args.infile, args.x, args.y)
    print(response)