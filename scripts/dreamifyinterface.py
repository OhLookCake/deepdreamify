import numpy as np
import scipy
from PIL import Image
import sys
import os
import getopt
import coredreamifier


#Image manipulation functions
def resize(image, maxdimension):
    print(image.shape)
    scale = 1.0 * maxdimension / max(image.shape[:2])
    transformedimage = scipy.misc.imresize(image, [int(round(scale * image.shape[0])), int(round(scale * image.shape[1]))])
    print(transformedimage.shape)
    return(transformedimage)



#Load image, and run deepdream

opts, args = getopt.getopt(sys.argv[1:], "f:r:e:", ["filename=", "resize_newsize=", "endlayer"])

filename = None
resize_newsize = None
#endlayer = 'inception_3b/5x5_reduce'
endlayer = 'inception_4c/output' #setting the default


for option, value in opts:
    if option in ("-f", "--filename"):
        filename = value
        title = os.path.basename(filename)
        title = '.'.join(title.split('.')[:-1])
    elif option in ("-r", "--resize_newsize"):
        resize_newsize = int(value)
        if resize_newsize <= 0:
            assert False, "Not a valid value for resizing: " + str(resize_newsize)
    elif option in ("-e", "--endlayer"):
        endlayer = value
        all_layers = net.blobs.keys()
        if endlayer not in all_layers:
            assert False, endlayer + " not a valid layer"
    else:
        assert False, "Unhandled option " + option

rawimage = np.float32(Image.open(filename))
print('Image Loaded')

#resize_newsize
if resize_newsize:
    image = resize(rawimage, resize_newsize)
    print('Image resized')
else:
    image = rawimage

net = coredreamifier.loadmodel()
_ = coredreamifier.deepdream(net, image, end=endlayer, outfile_prefix='output/'+title)



