import argparse
import logging
from shapely.geometry import Polygon
from polygon_utils.utils.utils import load_polygon_from_file, write_polygon_to_file, fill_multipolygon

def take_symmetric_difference(outer_poly, inner_poly):
    """
    Helper function to take the symmetric difference of two polygons by
    creating a hole in the outer polygon that corresponds to the inner polygon.
    """
    return Polygon(list(zip(*outer_poly.exterior.coords.xy)), holes=[list(zip(*inner_poly.exterior.coords.xy))])

def symmetric_difference_multipolygons(parent, child, outfile, eps):
    """
    Wrapper function to take the symmetric difference of two polygons by
    creating a hole in the polygon represented in parent that corresponds to the
    polygon represented by child.
    Eps is the degree of buffer around each point (a larger eps results in less accuracy).
    """
    parent_poly = load_polygon_from_file(parent)
    filled_parent = fill_multipolygon(parent_poly, eps)

    child_poly = load_polygon_from_file(child)
    filled_child = fill_multipolygon(child_poly, eps)

    difference_poly = take_symmetric_difference(filled_parent, filled_child)
    write_polygon_to_file(difference_poly, outfile)

if __name__ == '__main__':
    logging.basicConfig(format='[%(asctime)s] %(levelname)s:%(message)s', level=logging.DEBUG)
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--parent', help='file path to the geoJSON of the polygon to add a hole to')
    parser.add_argument('-c', '--child', help='file path to the geoJSON of the polygon to represent the hole')
    parser.add_argument('-o', '--outfile', help='file path to write the resulting multiploygon to')
    parser.add_argument('-e', '--eps', help='amount of buffer around points', default=0.0001, type=float)
    args = parser.parse_args()
    symmetric_difference_multipolygons(args.parent, args.child, args.outfile, args.eps)