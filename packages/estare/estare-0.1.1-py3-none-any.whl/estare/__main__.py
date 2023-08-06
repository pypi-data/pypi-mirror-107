
"""This script includes the entry point.

For more information on usage, run estare -h, or see the documentation.
"""

import numpy as np
from estare.src.init import examine, setup
from estare.src.feature import extract
from estare.src.align import align
from estare.src.scan import scan

from matplotlib import pyplot as plt
import argparse
import os
from skimage.io import imsave





def assemble(args):
    # unpack the arguments
    img_1 = args.layer_1
    img_2 = args.layer_2
    pivot_1 = args.feature_1
    pivot_2 = args.feature_2

    # align and stack the two input frames
    stacked_frame = align(img_1, img_2, pivot_1, pivot_2, save=True)

         
parser = argparse.ArgumentParser(prog='estare', description='''Program for aligning and stacking astro photos.''',
                                 epilog='''estare is a Persian word for star.''')

sub_parsers = parser.add_subparsers()

# create the parser for the feature detection command
parse_feature = sub_parsers.add_parser('scan', help='''Scan an input image to find suitable features such as (a) 
bright star(s) that can be used for aligning multiple frames.''')

parse_feature.add_argument('image', action='store', type=str,  help='The input image to be scanned.')
parse_feature.add_argument('kapa',  action='store', type=float, help='''Threshold for picking pixels 
of a certain brightness. It takes a floating point values from the range [0, 1]. Pick a larger value 
to limit the detected features to those of a higher brightness.''')
parse_feature.set_defaults(func=scan)

parse_stack = sub_parsers.add_parser('stack', help='''This mode should normally be used after running 
the scan mode whereby alignment features can be extracted. The stack mode uses the coordinates of two 
features shared in two frames to align them. It then adjusts them and stacks them up. Two input images 
along with two identical features for each image are required.''')

parse_stack.add_argument('layer_1', help='Path and name of the reference image (base layer)')
parse_stack.add_argument('layer_2', help='Path and name of the second image (top layer)')
parse_stack.add_argument('feature_1', help='''Path and name of a .npy file containing the coordinates 
of the feature in the reference layer''')
parse_stack.add_argument('feature_2', help='''Path and name of a .npy file containing the coordinates 
of the feature in the second layer which will be lined up with the reference layer.''')
parse_stack.set_defaults(func=assemble)

args = parser.parse_args()


if __name__ == '__main__':
    args = parser.parse_args()
    args.func(args)   # call the default function
