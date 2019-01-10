# -*- coding: utf-8 -*-
import cv2
from imutils import face_utils
import numpy as np
#import argparse
import imutils
import dlib
import math

class TN():

    def __init__(self,importframe,detector,predictor,preangle):
        self.angle = -1.0
        self.frame = importframe
        gray = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)
        rects = detector(gray, 0)
        for rect in rects:
            shape = predictor(gray, rect)
            shape = face_utils.shape_to_np(shape)

            (x, y, w, h) = face_utils.rect_to_bb(rect)
            cv2.rectangle(self.frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            #cv2.circle(self.frame, (x,y), 3, (0,255,0), 2)
        
            for (x,y) in shape:
                cv2.circle(self.frame, (x,y), 1, (0,0,255), 2)
    
            nose1=(int(shape[27][0]),int(shape[27][1]))
            nose2=(int(shape[30][0]),int(shape[30][1]))
            #cv2.line(self.frame,nose1,nose2,(0,255,0),2)
            eye1=(int(shape[36][0]),int(shape[36][1]))
            eye2=(int(shape[45][0]),int(shape[45][1]))
            cv2.line(self.frame,eye1,eye2,(0,255,0),2)

            x1=int(shape[36][0])
            y1=int(shape[36][1])
            x2=int(shape[45][0])
            y2=int(shape[45][1])
            disto=math.sqrt((math.fabs(x2-x1))**2+((math.fabs(y2-y1)))**2)
            distx=math.fabs(x2-x1)
            self.angle = np.arcsin((distx/disto))* 180/math.pi
            self.angle=90-self.angle
        if self.angle == -1.0:
            self.angle = preangle
        cv2.putText(self.frame, str("DEGREE : %.1f")%self.angle, (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
            