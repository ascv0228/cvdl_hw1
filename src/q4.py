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

class Q4Widget(QWidget):
    def __init__(self, baseLayout, parent=None):
        self.baseLayout = baseLayout
        super().__init__(parent)
        self.q4_layout = QVBoxLayout()
        
        load_image1_button = QPushButton('Load Image1')
        load_image2_button = QPushButton('Load Image2')
        get_keypoints_button = QPushButton('4.1 Keypoints')
        matched_keypoint_button = QPushButton('4.2 Matched Keypoints')
        
        load_image1_button.clicked.connect(self.load_image1)
        load_image2_button.clicked.connect(self.load_image2)
        get_keypoints_button.clicked.connect(self.get_keypoints)
        matched_keypoint_button.clicked.connect(self.matched_keypoint)


        self.q4_layout.addWidget(load_image1_button)
        self.q4_layout.addWidget(load_image2_button)
        self.q4_layout.addWidget(get_keypoints_button)
        self.q4_layout.addWidget(matched_keypoint_button)


    def load_image1(self):
        # Open file dialog to select an image file
        file_name, _ = QFileDialog.getOpenFileName(self, "Open Image File", "", "Images (*.png *.xpm *.jpg *.bmp *.gif)")
        if file_name:
            self.image1 = cv2.imread(file_name)

    def load_image2(self):
        # Open file dialog to select an image file
        file_name, _ = QFileDialog.getOpenFileName(self, "Open Image File", "", "Images (*.png *.xpm *.jpg *.bmp *.gif)")
        if file_name:
            self.image2 = cv2.imread(file_name)


    def get_keypoints(self):
        # TODO
        if self.image1 is not None:
            # Convert to grayscale
            gray = cv2.cvtColor(self.image1, cv2.COLOR_BGR2GRAY)
            
            # Create a SIFT detector
            sift = cv2.SIFT_create()
            
            # Detect keypoints and compute descriptors
            keypoints, descriptors = sift.detectAndCompute(gray, None)
            
            # Draw keypoints on the grayscale image
            img_with_keypoints = cv2.drawKeypoints(gray, keypoints, None, color=(0, 255, 0))
            
            # Display the image with keypoints
            self.showImageWindow(img_with_keypoints, "Keypoints")
            # self.showImageWindow(img_with_keypoints, "Keypoints")
            # cv2.imshow("kp", img_with_keypoints)
            # cv2.resizeWindow('kp', 800, 600)
        else:
            print("Please load Image 1 first")

    def matched_keypoint(self):
        # TODO
        try:
            if self.image1 is not None and self.image2 is not None:
                # Convert images to grayscale
                gray1 = cv2.cvtColor(self.image1, cv2.COLOR_BGR2GRAY)
                gray2 = cv2.cvtColor(self.image2, cv2.COLOR_BGR2GRAY)
                
                # Initialize SIFT detector
                sift = cv2.SIFT_create()
                
                # Detect keypoints and compute descriptors for both images
                keypoints1, descriptors1 = sift.detectAndCompute(gray1, None)
                keypoints2, descriptors2 = sift.detectAndCompute(gray2, None)


                
                # Match descriptors using BFMatcher with k=2 for knn
                bf = cv2.BFMatcher()
                matches = bf.knnMatch(descriptors1, descriptors2, k=2)
                
                # Apply ratio test to find good matches
                good_matches = []
                for m, n in matches:
                    if m.distance < 0.75 * n.distance:
                        good_matches.append([m])

                # Draw the good matches on the images
                img_matches = cv2.drawMatchesKnn(gray1, keypoints1, gray2, keypoints2, good_matches, None, flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)
                
                # Display the matched image
                self.showImageWindow(img_matches, "match keypoints")
        except Exception as e:
            print(e)
            print("Please load both images first")

    
    def showImageWindow(self, img, title):
        img_window = ImageWindow(img, title)
        # img_window.show()