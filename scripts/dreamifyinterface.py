import numpy as np
import scipy
from PIL import Image
import sys
import os
import getopt
import logging
import coredreamifier



#Image manipulation functions
def resize(image, maxdimension):
    print(image.shape)
    scale = 1.0 * maxdimension / max(image.shape[:2])
    transformedimage = scipy.misc.imresize(image, [int(round(scale * image.shape[0])), int(round(scale * image.shape[1]))])
    print(transformedimage.shape)
    return(transformedimage)


def dreamify(filename, resize_newsize=None, endlayer='inception_4c/output'):
    dreamlogger = logging.getLogger('dreamify')
    dreamlogger.info('Dreamifier initiated')

    #Load image, and run deepdream
    title = os.path.basename(filename)
    title = '.'.join(title.split('.')[:-1])
    net = coredreamifier.loadmodel()
    all_layers = net.blobs.keys()
    if endlayer not in all_layers:
        assert False, endlayer + " not a valid layer"

    rawimage = np.float32(Image.open(filename))
    dreamlogger.info('Image Loaded')

    #resize_newsize
    if resize_newsize:
        image = resize(rawimage, resize_newsize)
        dreamlogger.info('Image resized')
    else:
        image = rawimage
        dreamlogger.info('Image size retained')

    dreamlogger.info('Calling coredreamifier')
    _ = coredreamifier.deepdream(net, image, end=endlayer, outfile_prefix='images/processed/'+title)


