#!/usr/bin/python
import numpy as np
import cv
import freenect
import profundidad

cv.NamedWindow('Prueba')
print 'Para detener presiona Esc'

def get_depth():
    return profundidad.depth_cv(freenect.sync_get_depth()[0])

while 1:
    cv.ShowImage('Prueba', get_depth())
    if cv.WaitKey(10)==27:
        break
