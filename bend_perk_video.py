# -*- coding: utf-8 -*-
import cv2
import numpy as np
import math
import imutils

class UD():

    def findcolour(frame,colourlow,colourhi):
        blurred = cv2.GaussianBlur(frame, (11, 11), 0)
        colour = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
        kernel = np.ones((9,9),np.uint8)
        mask = cv2.inRange(colour, colourlow, colourhi)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
        #res = cv2.bitwise_and(frame, frame, mask=mask)
        cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
                                cv2.CHAIN_APPROX_SIMPLE)[-2]
        center = None
        if len(cnts)>0:
            c = max(cnts, key=cv2.contourArea)
            ((x, y), radius) = cv2.minEnclosingCircle(c)
            M = cv2.moments(c)
            center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
            if radius>0.01 :
                return center, radius
        else:
            return (2000,2000), -1.0
        

    def finddistance(x1,y1,x2,y2):
        dist=math.sqrt((math.fabs(x2-x1))**2+((math.fabs(y2-y1)))**2)
        return dist
        


    def __init__(self,importframe,preangle,predist,initial_angle):
        # colour range
        bluelow = np.array([97, 100, 117])
        bluehi = np.array([117, 255, 255])
        redlow = np.array([166, 84, 141])
        redhi = np.array([186, 255, 255])
        greenlow = np.array([40, 100, 50])
        greenhi = np.array([80,255,255])
        #greenlow = np.array([66, 122, 129])
        #greenhi = np.array([86,255,255])
        yellowlow = np.array([23, 59, 119])
        yellowhi = np.array([54,255,255])
        orangelow = np.array([0, 50, 80])
        orangehi = np.array([20,255,255])

        self.frame = importframe
        self.angle_neck_ear = -1.0
        self.dist_neck_ear = -1.0
        self.dist_ear_chin = -1.0
        self.angle_base = -1.0

        # BLUE represents EAR
        (bluex,bluey), bluerad = UD.findcolour(self.frame,bluelow,bluehi)
        if bluex!=2000 & bluey!=2000:
            cv2.circle(self.frame, (bluex, bluey), 20, (255, 0, 0), -1)
                
        # RED represents NECK
        (redx,redy), redrad = UD.findcolour(self.frame,redlow,redhi)
        if redx!=2000 & redy!=2000:
            cv2.circle(self.frame, (redx, redy), 20, (0, 0, 255), -1)
            #print(redrad)
        
        # GREEN represents CHIN
        (greenx,greeny), greenrad = UD.findcolour(self.frame,greenlow,greenhi)
        if greenx!=2000 & greeny!=2000:
            cv2.circle(self.frame, (greenx, greeny), 20, (0, 255, 0), -1)
        
        if redx!=2000 & redy!=2000 & greenx!=2000 & greeny!=2000 :
            dist_neck_ear = UD.finddistance(redx,redy,bluex,bluey)
            distx_neck_ear = math.fabs(redx-bluex)
            self.angle_neck_ear = np.arcsin((distx_neck_ear/dist_neck_ear))* 180/math.pi
            cv2.line(self.frame,(redx,redy),(bluex,bluey),(0,255,217),2)

        if redx!=2000 & redy!=2000 & greenx!=2000 & greeny!=2000 :
            A = float(redy-greeny)/float(redx-greenx)
            B = -1
            C = redy-a*redx

            dist_perpendicular = abs(A*bluex+B*bluey+C)/math.sqrt(A**2+B**2)
            dist_neck_ear = UD.finddistance(redx,redy,bluex,bluey)
            self.angle_base = np.arcsin((dist_perpendicular/dist_neck_ear))*180/math.pi


        if self.angle_neck_ear == -1.0:
            self.angle_neck_ear = preangle

        self.angle_display = abs(self.angle_neck_ear+self.angle_base-initial_angle)
        cv2.putText(self.frame, str("NECK-CHIN DEGREE: %.1f")%self.angle_display, (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
        self.angle = self.angle_neck_ear+self.angle_base

        if redx!=2000 & redy!=2000 & greenx!=2000 & greeny!=2000 & bluex!=2000 & bluey!=2000 :
            self.dist_neck_ear = UD.finddistance(redx,redy,bluex,bluey)
            self.dist_ear_chin = UD.finddistance(bluex,bluey,greenx,greeny)

        if self.dist_neck_ear == -1.0:
            self.dist_neck_ear = predist
        cv2.putText(self.frame, str("RED-BLUE cm: %.1f")%((1.88/redrad/2.0)*self.dist_neck_ear), (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)
        
        if self.dist_ear_chin == -1.0:
            self.dist_ear_chin = predist
        cv2.putText(self.frame, str("BLUE-GREEN cm: %.1f")%((1.88/redrad/2.0)*self.dist_ear_chin), (10, 100), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)