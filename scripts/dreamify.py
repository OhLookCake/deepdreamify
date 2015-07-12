import sys
import os
import numpy as np
import scipy.ndimage as nd
from PIL import Image
from google.protobuf import text_format
import caffe



def save_image(img, filename):
#    img8 = np.uint8(np.clip(img, 0, 255))
    img8 = np.uint8(img)
    img8 = Image.fromarray(img8)
    img8.save(filename)

# Functions for converting to and from Caffe's input image layout
def preprocess(net, img):
    return np.float32(np.rollaxis(img, 2)[::-1]) - net.transformer.mean['data']

def deprocess(net, img):
    return np.dstack((img + net.transformer.mean['data'])[::-1])

# Basic gradient ascent step function
def make_step(net, step_size=1.5, end='inception_4c/output', jitter=32, clip=True):
    '''Basic gradient ascent step.'''

    src = net.blobs['data'] # input image is stored in Net's 'data' blob
    dst = net.blobs[end]

    ox, oy = np.random.randint(-jitter, jitter+1, 2)
    src.data[0] = np.roll(np.roll(src.data[0], ox, -1), oy, -2) # apply jitter shift
            
    net.forward(end=end)
    dst.diff[:] = dst.data  # specify the optimization objective
    net.backward(start=end)
    g = src.diff[0]
    # apply normalized ascent step to the input image
    src.data[:] += step_size/np.abs(g).mean() * g

    src.data[0] = np.roll(np.roll(src.data[0], -ox, -1), -oy, -2) # unshift image
            
    if clip:
        bias = net.transformer.mean['data']
        src.data[:] = np.clip(src.data, -bias, 255-bias)

def deepdream(net, base_img, iter_n=10, octave_n=4, octave_scale=1.4, end='inception_4c/output', clip=True, outfile_prefix='image', **step_params):
    # prepare base images for all octaves
    octaves = [preprocess(net, base_img)]
    for i in xrange(octave_n-1):
        octaves.append(nd.zoom(octaves[-1], (1, 1.0/octave_scale,1.0/octave_scale), order=1))
    
    src = net.blobs['data']
    detail = np.zeros_like(octaves[-1]) # allocate image for network-produced details
    for octave, octave_base in enumerate(octaves[::-1]):
	print('Starting Octave ' + str(octave))
        h, w = octave_base.shape[-2:]
        if octave > 0:
            # upscale details from the previous octave
            h1, w1 = detail.shape[-2:]
            detail = nd.zoom(detail, (1, 1.0*h/h1,1.0*w/w1), order=1)

        src.reshape(1,3,h,w) # resize the network's input image size
        src.data[0] = octave_base+detail
        for i in xrange(iter_n):
            make_step(net, end=end, clip=clip, **step_params)
            
            # visualization
            vis = deprocess(net, src.data[0])
            if not clip: # adjust image contrast if clipping is disabled
                vis = vis*(255.0/np.percentile(vis, 99.98))
            save_image(vis, outfile_prefix + '_' + str(octave) + '_' + str(i) + '.jpg')
            print octave, i, end, vis.shape
            
            
        # extract details produced on the current octave
        detail = src.data[0]-octave_base
    # returning the resulting image
    return deprocess(net, src.data[0])



#Load Model
model_path = '../caffe/models/bvlc_googlenet/' # substitute your path here
net_fn   = model_path + 'deploy.prototxt'
param_fn = model_path + 'bvlc_googlenet.caffemodel'

print('Models loaded\n')

# Patching model to be able to compute gradients.
model = caffe.io.caffe_pb2.NetParameter()
text_format.Merge(open(net_fn).read(), model)
model.force_backward = True
open('tmp.prototxt', 'w').write(str(model))

net = caffe.Classifier('tmp.prototxt', param_fn,
                       mean = np.float32([104.0, 116.0, 122.0]), # ImageNet mean, training set dependent
                       channel_swap = (2,1,0)) # the reference model has channels in BGR order instead of RGB

print('Models patched')

all_layers = net.blobs.keys() 

#Load image, and run deepdream

if len(sys.argv) > 3:
    print('Usage:\npython dreamify.py <image> [<endlayer>]')
    sys.exit()

filename = sys.argv[1]
title = os.path.basename(filename)
title = '.'.join(title.split('.')[:-1])
rawimage = np.float32(Image.open(filename))
print('Image Loaded')


if len(sys.argv) == 3:
    endlayer = sys.argv[2]
    if endlayer not in all_layers:
        print endlayer + ' not an available layer name'
        sys.exit()
else:
    endlayer = 'inception_3b/5x5_reduce'


_ = deepdream(net, rawimage, end=endlayer, outfile_prefix='output/'+title)




