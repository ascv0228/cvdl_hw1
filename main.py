import sys
import glob
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QPushButton, QVBoxLayout, 
                             QHBoxLayout, QGridLayout, QGroupBox, QSpinBox, QLabel, QSpacerItem, QFileDialog)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap

from src import q1, q2, q3, q4
from src.ui_util import BaseWidget



class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('MainWindow')
        self.setGeometry(100, 100, 800, 600)
        
        # Create main layout
        main_layout = QGridLayout()
        # Load Image Group
        load_image_group = QGroupBox('Load Image')
        base = BaseWidget(parent=self)  # Pass self as the parent
        load_image_group.setLayout(base.base_layout)

        # # Calibration Group
        calibration_group = QGroupBox('1. Calibration')
        calibration_layout = q1.Q1Widget(base, parent=self)
        calibration_group.setLayout(calibration_layout.q1_layout)

        # Augmented Reality Group
        ar_group = QGroupBox('2. Augmented Reality')
        ar_layout = q2.Q2Widget(base, parent=self)
        ar_group.setLayout(ar_layout.q2_layout)

        # Stereo Disparity Map Group
        stereo_group = QGroupBox('3. Stereo disparity map')
        stereo_layout = q3.Q3Widget(base, parent=self)
        stereo_group.setLayout(stereo_layout.q3_layout)

        # SIFT Group
        sift_group = QGroupBox('4. SIFT')
        sift_layout = q4.Q4Widget(base, parent=self)
        sift_group.setLayout(sift_layout.q4_layout)

        # Add all groups to the main layout
        main_layout.addWidget(load_image_group, 0, 0)
        main_layout.addWidget(calibration_group, 0, 1)
        main_layout.addWidget(ar_group, 0, 2)
        main_layout.addWidget(stereo_group, 0, 3)
        main_layout.addWidget(sift_group, 1, 1)

                # Set column stretch to evenly distribute width
        main_layout.setColumnStretch(0, 1)
        main_layout.setColumnStretch(1, 1)
        main_layout.setColumnStretch(2, 1)
        main_layout.setColumnStretch(3, 1)

        
        # # Set row stretch so the bottom row also expands if needed
        main_layout.setRowStretch(0, 1)
        main_layout.setRowStretch(1, 1)

        # Create a central widget to hold the layout
        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        
        # # Set the central widget
        self.setCentralWidget(central_widget)
#
        # main_widget.setLayout(main_layout)
        # self.setCentralWidget(main_widget)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
