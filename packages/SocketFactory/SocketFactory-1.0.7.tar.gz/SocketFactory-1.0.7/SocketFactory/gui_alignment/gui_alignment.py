
from PyQt5.QtWidgets import *
from PyQt5.QtCore import pyqtSlot
import sys
import numpy as np
from SocketFactory.alignment import alignment_tt, alignment_tf
from SocketFactory.utilities import file_handler, utility

class AlignmentGui(QWidget):
    """
    Simple to align one or more meshes in a certain way.
    """

    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.initGUI()

    def initGUI(self):
        self.resize(400, 200)
        self.setWindowTitle('Alignment')

        self.mesh_paths = []
        self.mesh_label = QLabel("", self)
        mesh_btn = QPushButton("Load mesh files")

        self.landmark_paths = []
        self.landmark_label = QLabel("", self)
        landmark_btn = QPushButton("Load landmark files")

        self.alignment_path = ""
        self.alignment_label = QLabel("", self)
        alignment_btn = QPushButton("Load alignment file")

        radio_layout = QGridLayout()
        self.radiobutton_tt = QRadioButton("TT")
        self.radiobutton_tt.setChecked(True)
        self.radiobutton_tf = QRadioButton("TF")
        self.radiobutton_tf.setChecked(False)
        radio_layout.addWidget(self.radiobutton_tt, 0, 0)
        radio_layout.addWidget(self.radiobutton_tf, 0, 1)

        run_btn = QPushButton("Align")
        run_btn.setStyleSheet("background-color : orange")

        mesh_btn.clicked.connect(self.choose_meshes)
        landmark_btn.clicked.connect(self.choose_landmarks)
        alignment_btn.clicked.connect(self.choose_alignment)
        run_btn.clicked.connect(self.align)

        vbox = QVBoxLayout()
        vbox.addWidget(self.mesh_label)
        vbox.addWidget(mesh_btn)
        vbox.addWidget(self.landmark_label)
        vbox.addWidget(landmark_btn)
        vbox.addWidget(self.alignment_label)
        vbox.addWidget(alignment_btn)
        vbox.addLayout(radio_layout)
        vbox.addWidget(run_btn)
        self.setLayout(vbox)

    @pyqtSlot()
    def choose_meshes(self):
        self.mesh_paths, _ = QFileDialog.getOpenFileNames(self, 'Open file', filter = "Meshes (*.stl *.ply)")
        self.mesh_paths.sort()
        final_label = ''
        for n in self.mesh_paths:
             final_label += n.split("/")[-1] + '\n'
        self.mesh_label.setText(final_label)
        return

    @pyqtSlot()
    def choose_landmarks(self):
        self.landmark_paths, _ = QFileDialog.getOpenFileNames(self, 'Open file', filter = "Text (*.txt)")
        self.landmark_paths.sort()
        final_label = ''
        for n in self.landmark_paths:
             final_label += n.split("/")[-1] + '\n'
        self.landmark_label.setText(final_label)
        return
 
    @pyqtSlot()
    def choose_alignment(self):
        self.alignment_path, _ = QFileDialog.getOpenFileName(self, 'Open file', filter = "Text (*.txt)")
        self.alignment_label.setText(self.alignment_path.split("/")[-1])
        return

    @pyqtSlot()
    def align(self):
         method =  "TT" if (self.radiobutton_tt.isChecked()) else "TF"

         cut_point, reference_alignment_points, alignment_method, landmarks_names, origin = file_handler.read_alignment_file(self.alignment_path)
         self.parent.compile_form(cut_point, reference_alignment_points, alignment_method, landmarks_names, origin)
         output_files = []
         for mesh_path, landmark_path in zip(self.mesh_paths, self.landmark_paths) :
            mesh_vert = utility.read(mesh_path).GetPoints()
            lmk_dict = file_handler.read_points(landmark_path)
            landmarks_coordinates = utility.query_dict(lmk_dict, landmarks_names, mesh_vert) 

            origin_coordinates = () if (origin == "min") else utility.query_dict(lmk_dict, [origin], mesh_vert)[0]
            cut_point_coordinates =  utility.query_dict(lmk_dict, [cut_point], mesh_vert)[0]
            reference_points_coordinates = utility.query_dict(lmk_dict, reference_alignment_points, mesh_vert)

            if (method == "TT"):
                output_files.append(alignment_tt.align_sdr_tt(mesh_path, cut_point_coordinates, reference_points_coordinates, 
                                                landmarks_coordinates, origin_coordinates, method = alignment_method))
            elif (method == "TF"):
                output_files.append(alignment_tf.align_sdr_tf(mesh_path, cut_point_coordinates, reference_points_coordinates,
                                                 landmarks_coordinates, origin_coordinates, method = alignment_method))
         self.parent.add_output_meshes(output_files)
         