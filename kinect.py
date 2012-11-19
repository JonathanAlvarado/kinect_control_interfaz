#!/usr/bin/python
import numpy as np
import cv
import freenect

def first_depth(depth):
    #if an interval of [0, 1] is specified, values smaller than 0 become 0, and values larger than 1 become 1.
    np.clip(depth, 0, 2**10 - 1, depth)
    depth >>= 2
    depth = depth.astype(np.uint8)
    return depth

def depth_cv(depth):
    depth = first_depth(depth)
    image = cv.CreateImageHeader((depth.shape[1], depth.shape[0]),
                                 cv.IPL_DEPTH_8U,
                                 1)
    cv.SetData(image, depth.tostring(),
               depth.dtype.itemsize * depth.shape[1])
    return image

cv.NamedWindow('Prueba')
print 'Para detener presiona Esc'

def get_depth():
    return depth_cv(freenect.sync_get_depth()[0])

while 1:
    cv.ShowImage('Prueba', get_depth())
    if cv.WaitKey(10)==27:
        break
