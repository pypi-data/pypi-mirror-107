from PyQt5.QtWidgets import *
from PyQt5 import Qt
from PyQt5.QtCore import pyqtSlot
from SocketFactory.utilities import utility, file_handler
import numpy as np
import sys

class RBFFileGenerationGui(QWidget):
    """
    Simple gui to select reference and target mesh and their landmark files.
    """

    def __init__(self):
        super().__init__()
        self.initGUI()

    def initGUI(self):
        self.resize(400, 200)
        self.setWindowTitle('PTS file extraction')
        self.reference_label = QLabel('', self)
        reference_btn = QPushButton('Load reference mesh')
        self.reference_path = ""
        
        self.reference_landmark_label = QLabel('', self)
        reference_landmark_btn = QPushButton('Load reference landmarks')
        self.reference_landmark_path = ""

        self.target_label = QLabel('', self)
        target_btn = QPushButton('Load target mesh')
        self.target_path = ""

        self.target_landmark_label = QLabel('', self)
        target_landmark_btn = QPushButton('Load target landmarks')
        self.target_landmark_path = ""

        generate_file_btn = QPushButton('Generate .pts file', self)
        generate_file_btn.setStyleSheet("background-color : orange")

        reference_btn.clicked.connect(self.choose_reference)
        target_btn.clicked.connect(self.choose_target)
        reference_landmark_btn.clicked.connect(self.choose_reference_landmarks)
        target_landmark_btn.clicked.connect(self.choose_target_landmarks)
        generate_file_btn.clicked.connect(self.generate_file)

        vbox = QVBoxLayout()
        vbox.addWidget(self.reference_label)
        vbox.addWidget(reference_btn)
        vbox.addWidget(self.reference_landmark_label)
        vbox.addWidget(reference_landmark_btn)
        vbox.addWidget(self.target_label)
        vbox.addWidget(target_btn)
        vbox.addWidget(self.target_landmark_label)
        vbox.addWidget(target_landmark_btn)
        vbox.addWidget(generate_file_btn)
        self.setLayout(vbox)
        self.show()

    @pyqtSlot()
    def choose_reference(self):
        self.reference_path, _ = QFileDialog.getOpenFileName(self, 'Open file', filter = "Meshes (*.stl *.ply)")
        self.reference_label .setText(self.reference_path.split("/")[-1])
        return
   
    @pyqtSlot()
    def choose_reference_landmarks(self):
        self.reference_landmark_path, _ = QFileDialog.getOpenFileName(self, 'Open file', filter = "Text (*.txt)")
        self.reference_landmark_label .setText(self.reference_landmark_path.split("/")[-1])
        return

    @pyqtSlot()
    def choose_target(self):
        self.target_path, _ = QFileDialog.getOpenFileName(self, 'Open file', filter = "Meshes (*.stl *.ply)")
        self.target_label.setText(self.target_path.split("/")[-1])
        return

    @pyqtSlot()
    def choose_target_landmarks(self):
        self.target_landmark_path, _ = QFileDialog.getOpenFileName(self, 'Open file', filter = "Text (*.txt)")
        self.target_landmark_label.setText(self.target_landmark_path.split("/")[-1])
        return

    @pyqtSlot()
    def generate_file(self):
        self.close()
        file_handler.create_pts_file(self.reference_path, self.target_path, self.reference_landmark_path, self.target_landmark_path)


def launch():
    app = QApplication(sys.argv)
    window = RBFFileGenerationGui()
    sys.exit(app.exec_())
    
if __name__=='__main__':
    launch()

