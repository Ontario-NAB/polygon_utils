import argparse
import logging
from polygon_utils.utils.utils import load_polygon_from_file, write_polygon_to_file, fill_multipolygon


def fill_multipolygon_wrapper(infile, outfile, eps):
    """
    Wrapper function to encapsulate reading in polygon from file,
    filling the holes in the polygon, and writing the result to a file.
    """
    mp = load_polygon_from_file(infile)
    filled_mp = fill_multipolygon(mp, eps)
    write_polygon_to_file(filled_mp, outfile)


if __name__ == '__main__':
    logging.basicConfig(format='[%(asctime)s] %(levelname)s:%(message)s', level=logging.DEBUG)
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--infile', help='file path to the geoJSON of the polygon to fill')
    parser.add_argument('-o', '--outfile', help='file path to write the filled polygon to')
    parser.add_argument('-e', '--eps', help='amount of buffer around points', default=0.0001, type=float)
    args = parser.parse_args()
    fill_multipolygon_wrapper(args.infile, args.outfile, args.eps)