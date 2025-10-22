import cv2
import numpy as np
import sys
import glob
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QPushButton, QVBoxLayout, 
                             QHBoxLayout, QGridLayout, QGroupBox, QSpinBox, QLabel, QSpacerItem, 
                             QLineEdit, QFileDialog, QTextEdit)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QImage
import os


class Q2Widget(QWidget):
    def __init__(self, baseLayout, parent=None):
        self.baseLayout = baseLayout
        super().__init__(parent)
        self.q2_layout = QVBoxLayout()
        
        self.text_box = QLineEdit()
        self.text_box.resize(100, 20)
        show_on_board_button = QPushButton('2.1 show words on board')
        show_vertical_button = QPushButton('2.2 show words vertical')
        
        show_on_board_button.clicked.connect(self.show_on_board)
        show_vertical_button.clicked.connect(self.show_vertical)

        self.q2_layout.addWidget(self.text_box)
        self.q2_layout.addWidget(show_on_board_button)
        self.q2_layout.addWidget(show_vertical_button)
        # self.q2_layout.resize()

    def show_on_board(self):
        # text = self.text_box.text()
        # TODO
        width, height = 11, 8
        self.ImagePoints=list()
        self.ObjectPoints=list()
        objpoint=np.zeros((width*height,3),np.float32)
        objpoint[:,:2]=np.mgrid[0:width,0:height].T.reshape(-1, 2)
        #print(self.ObjectPoints)
        for i in range(len(self.baseLayout.images)):
            #print(self.filestr[i])
            img = cv2.imread(os.path.join(self.baseLayout.folder_path, f"{i+1}.bmp"))
            # winname=str(i+1)+'.bmp'
            grayimg=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
            ret,corners=cv2.findChessboardCorners(grayimg, (width, height), None)

            #print(corners)
            #print("ret",ret)
            #print("corners",corners)
            if ret:
                self.ImagePoints.append(corners)
                self.ObjectPoints.append(objpoint)
        offsets =[[7.0, 5.0, 0.0], [4.0, 5.0, 0.0], [1.0, 5.0, 0.0], [7.0, 2.0, 0.0], [4.0, 2.0, 0.0], [1.0, 2.0, 0.0]]
        ret,mat_intri,cof_dist,v_rot,v_trans=cv2.calibrateCamera (self.ObjectPoints, self.ImagePoints,(width, height) ,None, None)
        # text=self.ui.textEdit.toPlainText()
        text = self.text_box.text()
        fs = cv2.FileStorage(os.path.join(self.baseLayout.folder_path, "Q2_db", 'alphabet_db_onboard.txt'), cv2.FILE_STORAGE_READ)
        if text:
            for j in range(len(self.baseLayout.images)):
                img = cv2.imread(os.path.join(self.baseLayout.folder_path, f"{j+1}.bmp"))
                for i in range(len(text)):
                    ch_mat = fs.getNode(text[i]).mat()
                    ch_mat=np.float32(ch_mat).reshape(-1,3)
                    #print('before',ch_mat)
                    ch_mat=ch_mat+offsets[i]
                    #print('after',ch_mat)
                    img_points, jac = cv2.projectPoints(ch_mat, v_rot[j], v_trans[j], mat_intri, cof_dist)
                    for k in range(len(img_points)//2):
                        pt1=tuple(map(int,img_points[2*k].ravel()))
                        pt2=tuple(map(int,img_points[2*k+1].ravel()))
                        img = cv2.line(img, pt1, pt2, (0, 0, 255), 5)
                        
                img=cv2.resize(img,(1000,800))
                cv2.imshow('AR {}.bmp'.format(j+1),img)
                cv2.moveWindow('AR {}.bmp'.format(j+1),150,120)
                cv2.waitKey(1000)
                cv2.destroyAllWindows() 


    def show_vertical(self):
        # text = self.text_box.text()
        # TODO
        width, height = 11, 8
        self.ImagePoints=list()
        self.ObjectPoints=list()
        objpoint=np.zeros((width*height,3),np.float32)
        objpoint[:,:2]=np.mgrid[0:width,0:height].T.reshape(-1, 2)
        #print(self.ObjectPoints)
        for i in range(len(self.baseLayout.images)):
            #print(self.filestr[i])
            img = cv2.imread(os.path.join(self.baseLayout.folder_path, f"{i+1}.bmp"))
            # winname=str(i+1)+'.bmp'
            grayimg=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
            ret,corners=cv2.findChessboardCorners(grayimg, (width, height), None)

            #print(corners)
            #print("ret",ret)
            #print("corners",corners)
            if ret:
                self.ImagePoints.append(corners)
                self.ObjectPoints.append(objpoint)
        offsets =[[7.0, 5.0, 0.0], [4.0, 5.0, 0.0], [1.0, 5.0, 0.0], [7.0, 2.0, 0.0], [4.0, 2.0, 0.0], [1.0, 2.0, 0.0]]
        ret,mat_intri,cof_dist,v_rot,v_trans=cv2.calibrateCamera (self.ObjectPoints, self.ImagePoints,(width, height) ,None, None)
        # text=self.ui.textEdit.toPlainText()
        text = self.text_box.text()
        fs = cv2.FileStorage(os.path.join(self.baseLayout.folder_path, "Q2_db", 'alphabet_db_vertical.txt'), cv2.FILE_STORAGE_READ)

        if text:
            for j in range(len(self.baseLayout.images)):
                img = cv2.imread(os.path.join(self.baseLayout.folder_path, f"{j+1}.bmp"))
                for i in range(len(text)):
                    ch_mat = fs.getNode(text[i]).mat()
                    ch_mat=np.float32(ch_mat).reshape(-1,3)
                    #print('before',ch_mat)
                    ch_mat=ch_mat+offsets[i]
                    #print('after',ch_mat)
                    img_points, jac = cv2.projectPoints(ch_mat, v_rot[j], v_trans[j], mat_intri, cof_dist)
                    for k in range(len(img_points)//2):
                        pt1=tuple(map(int,img_points[2*k].ravel()))
                        pt2=tuple(map(int,img_points[2*k+1].ravel()))
                        img = cv2.line(img, pt1, pt2, (0, 0, 255), 5)
                        
                img=cv2.resize(img,(1000,800))
                cv2.imshow('AR {}.bmp'.format(j+1),img)
                cv2.moveWindow('AR {}.bmp'.format(j+1),150,120)
                cv2.waitKey(1000)
                cv2.destroyAllWindows()    
