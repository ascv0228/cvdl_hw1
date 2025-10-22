import cv2
import numpy as np
import sys
import glob
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QPushButton, QVBoxLayout, 
                             QHBoxLayout, QGridLayout, QGroupBox, QSpinBox, QLabel, QSpacerItem, 
                             QLineEdit, QFileDialog)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QImage

from src.ui_util import ImageWindow


def computeDisparity(imgL_path, imgR_path):
    imgL = cv2.imread(imgL_path, cv2.IMREAD_GRAYSCALE)
    imgR = cv2.imread(imgR_path, cv2.IMREAD_GRAYSCALE)

    # Create the StereoBM object
    stereo = cv2.StereoBM_create(numDisparities=432, blockSize=25)
    
    # Compute the disparity map
    disparity = stereo.compute(imgL, imgR)
    
    # Normalize the disparity map to 8-bit
    disp_norm = cv2.normalize(disparity, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)

    return disp_norm


class Q3Widget(QWidget):
    def __init__(self, baseLayout, parent=None):
        self.baseLayout = baseLayout
        super().__init__(parent)
        stereo_disparity_button = QPushButton('3.1 stereo disparity map')
        
        stereo_disparity_button.clicked.connect(self.stereo_disparity)

        
        self.q3_layout = QVBoxLayout()
        self.q3_layout.addWidget(stereo_disparity_button)

    def stereo_disparity(self):
        # Hint:
        #     Use OpenCV StereoBM class to build StereoBM objects.
        #     stereo = cv2.StereoBM.create(numDisparities=432, blockSize=25)
        #     disparity (Output) = stereo.compute(imgL,imgR) (Input)
        #     Show the Disparity Map (the value must be normalized to [0, 255])
        #     The above parameters can be freely changed according to the following rules.
        #     numDisparities (int): The disparity search range must be positive and divisible by 16.
        #     blockSize (int): The size of blocks compared by the algorithm, must be odd and within the range [5, 51]. 
        #     Larger block size implies smoother but less accurate disparity map. 
        #     Smaller block size gives finer disparity details, yet increase the likelihood of algorithmic misalignment.
        
        if self.baseLayout.imageL is None or self.baseLayout.imageR is None:
            print("Please load both images first!")
            return
        
        disp_norm = computeDisparity(self.baseLayout.imageL, self.baseLayout.imageR)
        
        # imgL = cv2.cvtColor(cv2.imread(self.baseLayout.imageL, cv2.IMREAD_COLOR), cv2.COLOR_BGR2RGB)
        # imgR = cv2.cvtColor(cv2.imread(self.baseLayout.imageR, cv2.IMREAD_COLOR), cv2.COLOR_BGR2RGB)
        imgL = cv2.imread(self.baseLayout.imageL, cv2.IMREAD_COLOR)
        imgR = cv2.imread(self.baseLayout.imageR, cv2.IMREAD_COLOR)
        

        self.showImageWindow(imgL, "ImgL")
        self.showImageWindow(imgR, "ImgR")
        self.showImageWindow(disp_norm, "Disparity Map")
    
    def showImageWindow(self, img, title):
        img_window = ImageWindow(img, title)