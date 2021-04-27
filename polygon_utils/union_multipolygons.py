import argparse
import logging
from shapely.geometry import Polygon
from shapely.ops import cascaded_union
from polygon_utils.utils.utils import load_polygon_from_file, write_polygon_to_file, fill_multipolygon

def multipolygon_union(polygon_list):
    """
    Helper function to take a list of adjacent polygons and union them into one large polygon.
    This method will log an error if the polygons cannot be unioned (e.g. they are not adjacent).
    """
    try:
        u = cascaded_union(polygon_list)
        return Polygon(list(zip(*u.exterior.coords.xy)))
    except Exception as err:
        logging.error(err)
        return None

def union_multipolygons_wrapper(infile, outfile, eps):
    """
    Wrapper function to read multiple polygons from the semicolon separated infile string,
    union them if possible, and write the result to outfile.
    Eps is the degree of buffer around each point (a larger eps results in less accuracy).
    """
    infiles = infile.split(';')
    if len(infiles) <= 1:
        logging.error('At least two files must be provided for union.')
    else:
        polygons = []
        for file_name in infiles:
            mp = load_polygon_from_file(file_name)
            polygons.append(fill_multipolygon(mp, eps))
        write_polygon_to_file(multipolygon_union(polygons), outfile)

if __name__ == '__main__':
    logging.basicConfig(format='[%(asctime)s] %(levelname)s:%(message)s', level=logging.DEBUG)
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--infile', help='semicolon separated list of file paths to the geoJSON of the polygons to union')
    parser.add_argument('-o', '--outfile', help='file path to write the unioned polygon to')
    parser.add_argument('-e', '--eps', help='amount of buffer around points', default=0.0001, type=float)
    args = parser.parse_args()
    union_multipolygons_wrapper(args.infile, args.outfile, args.eps)