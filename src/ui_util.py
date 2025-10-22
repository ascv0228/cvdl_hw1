import sys
import glob
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QPushButton, QVBoxLayout, 
                             QHBoxLayout, QGridLayout, QGroupBox, QSpinBox, QLabel, QSpacerItem, 
                             QLineEdit, QFileDialog)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QImage
import numpy as np
import cv2

class BaseWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        load_folder_button = QPushButton('Load folder')
        load_imageL_button = QPushButton('Load Image_L')
        load_imageR_button = QPushButton('Load Image_R')
        load_folder_button.clicked.connect(self.load_folder)
        load_imageL_button.clicked.connect(self.load_imageL)
        load_imageR_button.clicked.connect(self.load_imageR)

        self.base_layout = QVBoxLayout()
        self.base_layout.addWidget(load_folder_button)
        self.base_layout.addWidget(load_imageL_button)
        self.base_layout.addWidget(load_imageR_button)

    def load_folder(self):
        folder_path = QFileDialog.getExistingDirectory(self, "Select Folder Containing Images")
        if folder_path:
            self.images = glob.glob(folder_path + "/*.bmp")
            self.folder_path = folder_path

    def load_imageL(self):
        # Open file dialog to select an image file
        file_name, _ = QFileDialog.getOpenFileName(self, "Open Image File", "", "Images (*.png *.xpm *.jpg *.bmp *.gif)")
        if file_name:
            self.imageL = file_name

    def load_imageR(self):
        # Open file dialog to select an image file
        file_name, _ = QFileDialog.getOpenFileName(self, "Open Image File", "", "Images (*.png *.xpm *.jpg *.bmp *.gif)")
        if file_name:
            self.imageR = file_name



class ImageWindow():
    def __init__(self, img, title):
        height = img.shape[0]
        width = img.shape[1]
        resized_image = cv2.resize(img, (int(width/height)*500, 500))
        cv2.imshow(title, resized_image)



