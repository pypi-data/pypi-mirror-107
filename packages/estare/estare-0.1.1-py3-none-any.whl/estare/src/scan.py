"""This module should be imported by the entry point script.

It implements the function scan that is used for detecting 
features that are suitable for aligning two images.  
"""

from estare.src.init import examine, setup
from estare.src.feature import extract
from matplotlib import pyplot as plt
from skimage.io import imsave

import os
import numpy as np


def scan(args):
    """Finds features that are suitable for aligning two images.

    This function shows the input image in a graph first. It then 
    goes through every pixel of it and compares its brightness with 
    a given threshold (kapa) specified by the user. If the pixel's 
    brightness is higher than or equal to the threshold, a marker 
    will be shown on that location in the graph and the user can 
    accept it as a feature by pressing any key. The pixel can 
    alternatively be discarded by a left click.

    Args:
        args : user inputs parsed by argparse
    """
    
    # handle input arguments
    imagePath = args.image
    threshold = args.kapa

    img_as_array, x_range, y_range = examine(imagePath, save=True, verbose=False, graphics=False)
    # Replace with:
    # img_as_array = FloatImage(imagePath)
    # img_as_array.print_info()
    # img_as_array.save()
    # x_range, y_range = img_as_array.size()
    
    print(f'Image has x-range = {x_range}, and y-range = {y_range}')

    imgGray = img_as_array @ [0.2126, 0.7152, 0.0722]  # image in grayscale
    # Replace with (makes FloatImage redundant):
    # imgGray = GrayImage(imagePath)
    # imgGray.print_info()
    # imgGray.save()
    # x_range, y_range = imgGray.size()

    fig2, frame = plt.subplots(1, 1)
    image_features = frame.imshow(imgGray, cmap='gray')
    frame.set_title('Marked features', fontsize=14)

    numFeatures, indices, markers = extract(imgGray, xRng=[0, x_range], yRng=[0, y_range],
                                            kapa=threshold)
    # Replace with:
    # numFeatures, indices, markers = imgGray.extract(xRng=[0, x_range], yRng=[0, y_range], kapa=threshold)

    print(f'''
    Total number of features detected: {numFeatures}. If this is too many, consider increasing  
    the threshold input.
    ''')

    # Loop over features and ask the user if a feature is of interest to be saved
    keepFeature = False

    xy_FeatureCount = 0   # number of already-saved feature coordinates initialized to zero
    binFeatureCount = 0   # number of already-saves feature images in binary format initialized to zero
    imgFeatureCount = 0   # number of already-saves feature images in .png format initialized to zero

    xy_RefusedCount = 0   # number of already-saved refused coordinates initialized to zero
    binRefusedCount = 0   # number of already-saves refused images in binary format initialized to zero
    imgRefusedCount = 0   # number of already-saves refused images in .png format initialized to zero  

    for files in os.listdir('./data/features'):
        if files.endswith('.png'):
            imgFeatureCount += 1

    for files in os.listdir('./data/features/pixels'):
        if files.endswith('.npy'):
            binFeatureCount += 1

    for files in os.listdir('./data/features/coordinates'):
        if files.endswith('.npy'):
            xy_FeatureCount += 1


    for files in os.listdir('./data/refuse'):
        if files.endswith('.png'):
            imgRefusedCount += 1

    for files in os.listdir('./data/refuse/pixels'):
        if files.endswith('.npy'):
            binRefusedCount += 1

    for files in os.listdir('./data/refuse/coordinates'):
        if files.endswith('.npy'):
            xy_RefusedCount += 1    
            
    selectedFeatures = 0  # counter
    refusedFeatures = 0  # counter
    
    
    # TODO: add a feature to use matplotlib.ginput
    if numFeatures > 0:
        print('''A detected feature is displayed by a black square. Press any key to save the current feature, or click 
        the mouse to discard it...''')
        for pair_0, pair_1 in zip(indices[0], indices[1]):
            if pair_0 > 3 and pair_1 > 3:
                arrow = frame.annotate('O', xy=(pair_1, pair_0), arrowprops=dict(color='lime',arrowstyle='->'))
                plt.draw()  # , plt.pause(0.01)
                btnpress = plt.waitforbuttonpress(-1)
                if btnpress:
                    selectedFeatures += 1
                    np.save('./data/features/coordinates/feature_{}'.format(xy_FeatureCount), [pair_0, pair_1])
                    xy_FeatureCount += 1
                    np.save('./data/features/pixels/feature_{}_pixels'.format(binFeatureCount), imgGray[pair_0-10:pair_0+10, pair_1-10:pair_1+10])
                    binFeatureCount += 1
                    imsave('./data/features/feature_{}_pixels.png'.format(imgFeatureCount), imgGray[pair_0-10:pair_0+10, pair_1-10:pair_1+10])
                    imgFeatureCount += 1
                    # TODO: Find install path and cd to data
                    plt.waitforbuttonpress(0.1)
                else:
                    refusedFeatures += 1
                    np.save('./data/refuse/coordinates/refused_{}'.format(xy_RefusedCount), [pair_0, pair_1])
                    xy_RefusedCount += 1
                    np.save('./data/refuse/pixels/refused_{}_pixels'.format(binRefusedCount), imgGray[pair_0-10:pair_0+10, pair_1-10:pair_1+10])
                    binRefusedCount += 1
                    imsave('./data/refuse/refused_{}_pixels.png'.format(imgRefusedCount), imgGray[pair_0-10:pair_0+10, pair_1-10:pair_1+10])
                    imgRefusedCount += 1
                arrow.remove()   # removing the arrow must be the last thing to do at the end of the if-block
                
    print('Feature detection completed.')
    plt.show()
