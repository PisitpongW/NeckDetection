import sys

import cv2
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.uic import loadUi

from imutils import face_utils
import numpy as np
import imutils
import dlib
import math
import tilt_left_right_video
import rotate_left_right_video
import bend_perk_video
import frame_calibrate

class Team(QMainWindow):
    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor("D:\Work\Image_Processing\Class_project\shape_predictor_68_face_landmarks.dat")
    preangle = -1.0
    predist = -1.0
    initial_angle = 0.0
    displayangle = -1.0
    def __init__(self):
        super(Team,self).__init__()
        loadUi('graphic.ui',self)
        self.image=None
        self.S1.clicked.connect(self.start_webcam)

    def stop_webcam(self):
        self.timer.stop()

    def start_webcam(self):
        self.capture=cv2.VideoCapture(0)
        self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT,480)
        self.capture.set(cv2.CAP_PROP_FRAME_WIDTH,640)

        self.timer=QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(5)

    def update_frame(self):
        ret,self.frame=self.capture.read()
        self.frame = frame_calibrate.main(self.frame)

        if self.TN.isChecked() == True:
            x = tilt_left_right_video.TN(self.frame,Team.detector,Team.predictor,Team.preangle)
            Team.preangle = x.angle
            self.S2.clicked.connect(self.stop_webcam)
        if self.RL.isChecked() == True:
            x = rotate_left_right_video.RL(self.frame,Team.detector,Team.predictor,Team.preangle)
            Team.preangle = x.angle
            self.S2.clicked.connect(self.stop_webcam)
        if self.UD.isChecked() == True:
            x = bend_perk_video.UD(self.frame,Team.preangle,Team.predist,Team.initial_angle)
            Team.preangle = x.angle
            Team.predist = x.dist_ear_chin
            self.S2.clicked.connect(self.stop_webcam)
        
        Team.displayangle = x.angle
        self.Right.clicked.connect(self.r_display)
        self.Left.clicked.connect(self.l_display)
        self.Right2.clicked.connect(self.r2_display)
        self.Left2.clicked.connect(self.l2_display)
        self.Ref.clicked.connect(self.ref_display)
        self.Dorsal.clicked.connect(self.dor_display)
        self.Ventral.clicked.connect(self.ven_display)

        self.displayImage(x.frame,1)

    def displayImage(self,img,window=1):
        qformat=QImage.Format_Indexed8
        if len(img.shape)==3 :
            if img.shape[2]==4 :
                qformat=QImage.Format_RGBA8888
            else:
                qformat=QImage.Format_RGB888

        outImage=QImage(img,img.shape[1],img.shape[0],img.strides[0],qformat)
        #BGR to RGB
        outImage=outImage.rgbSwapped()

        if window==1:
            self.imgLabel.setPixmap(QPixmap.fromImage(outImage))
            self.imgLabel.setScaledContents(True)

    def r_display(self):
        self.r.display(Team.displayangle)

    def l_display(self):
        self.l.display(Team.displayangle)

    def r2_display(self):
        self.r2.display(Team.displayangle)

    def l2_display(self):
        self.l2.display(Team.displayangle)

    def ref_display(self):
        self.ref.display(Team.displayangle)
        Team.initial_angle = Team.displayangle

    def dor_display(self):
        self.dor.display(Team.displayangle)

    def ven_display(self):
        self.ven.display(Team.displayangle)
        

if __name__=='__main__':
    app=QApplication(sys.argv)
    window=Team()
    window.setWindowTitle('Neck Angle Detection')
    window.show()
    sys.exit(app.exec_())