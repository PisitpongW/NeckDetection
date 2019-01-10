import cv2
import numpy as np
import imutils

def main(frame):
    mtx = np.array([[963.26754941,   0.        , 507.37646707],
                    [  0.        , 967.0917043 , 382.58608893],
                    [  0.        ,   0.        ,   1.        ]])
    newcameramtx = np.array([[956.01782227,   0.        , 505.03593976],
                         [  0.        , 962.92492676, 388.82358581],
                         [  0.        ,   0.        ,   1.        ]])
    dist = np.array([[ 0.09058835, -0.4811732,   0.0099546,  -0.00238653,  0.63201972]])
    roi = (7, 5, 946, 713)
    frame = cv2.flip(frame, 1)
    #frame = cv2.resize(frame, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_AREA)
    frame = imutils.resize(frame, width=960, height=720)
    dst = cv2.undistort(frame, mtx, dist, None, newcameramtx)
    x,y,w,h = roi
    frame = dst[y:y+h, x:x+w]
    frame = imutils.resize(frame, width=640, height=480)
    return frame