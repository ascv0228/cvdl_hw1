import cv2
import numpy as np
import sys
import glob
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QPushButton, QVBoxLayout, 
                             QHBoxLayout, QGridLayout, QGroupBox, QSpinBox, QLabel, QSpacerItem, 
                             QLineEdit, QFileDialog, QMessageBox)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QImage
import os

# class Q1:
#     def __init__(self):
#         self.corners = None
#         self.rvec = None
#         self.tvec = None
#         self.dist = None
#         self.width, self.height = 11, 8



#     # 1.1 Corner detection
#     # def CornerDetection(self, grayimg):
#     #     width, height = 11, 8
#     #     ret, corners = cv2.findChessboardCorners(grayimg, (width, height))

#     #     if ret:
#     #         # Refine the corner positions
#     #         winSize = (5, 5)
#     #         zeroZone = (-1, -1)
#     #         criteria = (cv2.TERM_CRITERIA_MAX_ITER + cv2.TERM_CRITERIA_EPS, 30, 0.001)
#     #         self.corners = cv2.cornerSubPix(grayimg, corners, winSize, zeroZone, criteria)
#     #         return self.corners
#     #     else:
#     #         print("Corners not found")
#     #         return None

#     # 1.2 Find intrinsic parameters
#     def FindIntrinsic(self, objectPoints, imageSize=(2048, 2048)):
#         if self.corners is None:
#             print("No corners detected.")
#             return None
#         ret, ins, dist, rvec, tvec = cv2.calibrateCamera(objectPoints, self.corners, imageSize, None, None)
#         self.dist = dist
#         self.rvec = rvec
#         self.tvec = tvec
#         return ins, dist

#     # 1.3 Find extrinsic parameters
#     def FindExtrinsic(self):
#         if self.rvec is None or self.tvec is None:
#             print("No intrinsic data available.")
#             return None
#         rotation_matrix, _ = cv2.Rodrigues(self.rvec[0])
#         extrinsic_matrix = np.hstack((rotation_matrix, self.tvec[0]))
#         return extrinsic_matrix

#     # 1.4 Distortion matrix
#     def DistortionMatrix(self):
#         return self.dist if self.dist is not None else "Distortion not calculated"


class Q1Widget(QWidget):
    def __init__(self, baseLayout, parent=None):
        self.baseLayout = baseLayout
        # self.q1 = Q1()
        super().__init__(parent)
        self.q1_layout = QVBoxLayout()

        find_corners_button = QPushButton('1.1 Find corners')
        find_intrinsic_button = QPushButton('1.2 Find intrinsic')

        extrinsic_layout = QVBoxLayout()
        extrinsic_layout.addWidget(QLabel('1.3 Find extrinsic'))
        self.find_extrinsic_spinbox = QSpinBox()
        # extrinsic_layout.addWidget(QSpinBox())
        self.find_extrinsic_spinbox.setRange(1, 15)
        find_extrinsic_button = QPushButton('1.3 Find extrinsic')
        extrinsic_layout.addWidget(self.find_extrinsic_spinbox)
        extrinsic_layout.addWidget(find_extrinsic_button)


        find_distortion_button = QPushButton('1.4 Find distortion')
        show_result_button = QPushButton('1.5 Show result')

        find_corners_button.clicked.connect(self.find_corners)
        find_intrinsic_button.clicked.connect(self.find_intrinsic)
        find_extrinsic_button.clicked.connect(self.find_extrinsic)
        find_distortion_button.clicked.connect(self.find_distortion)
        show_result_button.clicked.connect(self.show_result)

        self.q1_layout.addWidget(find_corners_button)
        self.q1_layout.addWidget(find_intrinsic_button)
        self.q1_layout.addLayout(extrinsic_layout)
        self.q1_layout.addWidget(find_distortion_button)
        self.q1_layout.addWidget(show_result_button)

    def find_corners(self):
        self.ImagePoints=list()
        self.ObjectPoints=list()
        
        width, height = 11, 8
        objpoint=np.zeros((width*height,3),np.float32)
        objpoint[:,:2]=np.mgrid[0:width,0:height].T.reshape(-1, 2)
        print(self.baseLayout.images)
        #print(self.ObjectPoints)
        for images in self.baseLayout.images:
            #print(self.filestr[i])
            img = cv2.imread(images)
            # winname=str(i+1)+'.bmp'
            grayimg=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
            ret,corners=cv2.findChessboardCorners(grayimg, (width, height), None)

            #print(corners)
            #print("ret",ret)
            #print("corners",corners)
            if ret:
                winSize = (5, 5)
                zeroZone = (-1, -1)
                criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
                self.ImagePoints.append(corners)
                self.ObjectPoints.append(objpoint)
                cv2.cornerSubPix(grayimg, corners, winSize, zeroZone, criteria)
                img=cv2.cvtColor(grayimg,cv2.COLOR_GRAY2RGB)
                cv2.drawChessboardCorners(img, (width, height), corners, ret)
                #print('hello')
                img=cv2.resize(img,(1000,800))
                cv2.imshow(images,img)
                cv2.moveWindow(images,150,120)
                cv2.waitKey(650)
                cv2.destroyAllWindows() 

    def find_intrinsic(self):
        width, height = 11, 8
        ret, ins, cof_dist, v_rot, v_trans = cv2.calibrateCamera (self.ObjectPoints, self.ImagePoints,(width, height) ,None, None)
        if ret:
            print("Intrinsic:", ins)
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setText(np.array2string(ins))
            # msg.setInformativeText('More information')
            msg.setWindowTitle("Intrinsic")
            msg.exec_()

    def find_extrinsic(self):
        width, height = 11, 8
        ret,mat_intri,cof_dist,v_rot,v_trans=cv2.calibrateCamera(self.ObjectPoints, self.ImagePoints,(width, height) ,None, None)
        num = self.find_extrinsic_spinbox.value()
        filename = os.path.join(self.baseLayout.folder_path, f"{num}.bmp")
        print(filename)
        img = cv2.imread(filename)
        grayimg=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        winSize = (5, 5)
        zeroZone = (-1, -1)
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
        corners=cv2.cornerSubPix(grayimg, self.ImagePoints[num], winSize, zeroZone, criteria)
        ret,v_rot,v_trans=cv2.solvePnP(self.ObjectPoints[num],corners,mat_intri,cof_dist)
        Rotation_matrix,_=cv2.Rodrigues(v_rot)
        Extrinsic_matrix=np.column_stack((Rotation_matrix,v_trans))
        print(f'Extrinsic {num}.bmp:')
        print(Extrinsic_matrix)
        
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText(np.array2string(Extrinsic_matrix))
        # msg.setInformativeText('More information')
        msg.setWindowTitle(f'Extrinsic {num}.bmp:')
        msg.exec_()

    def find_distortion(self):
        
        width, height = 11, 8
            
        ret,mat_intri,cof_dist,v_rot,v_trans=cv2.calibrateCamera(self.ObjectPoints, self.ImagePoints,(width, height) ,None, None)
        if ret:
            print("Distortion:")
            print(cof_dist)
            
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setText(np.array2string(cof_dist))
            # msg.setInformativeText('More information')
            msg.setWindowTitle(f'Distortion:')
            msg.exec_()
        # print("Distortion matrix:", distortion)

    def show_result(self):
        # Placeholder for displaying results
        
        width, height = 11, 8
        ret,mat_intri,cof_dist,v_rot,v_trans=cv2.calibrateCamera (self.ObjectPoints, self.ImagePoints,(width, height) ,None, None) 
        for i in range(len(self.baseLayout.images)):
            img = cv2.imread(os.path.join(self.baseLayout.folder_path, f"{i+1}.bmp"))
            undistorted_img=cv2.undistort(img,mat_intri,cof_dist)
            concatenated_img=np.hstack([img,undistorted_img])
            concatenated_img=cv2.resize(concatenated_img,(1500,800))
            cv2.imshow('{}.bmp-Distorted(left) vs undistorted(right)'.format(i+1),concatenated_img)
            cv2.moveWindow('{}.bmp-Distorted(left) vs undistorted(right)'.format(i+1),150,120)
            cv2.waitKey(650)
            cv2.destroyAllWindows()
