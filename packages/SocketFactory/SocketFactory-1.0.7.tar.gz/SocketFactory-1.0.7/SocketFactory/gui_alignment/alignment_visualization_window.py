
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import Qt
from PyQt5.QtCore import pyqtSlot
import sys
import vtk
from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
import numpy as np
import itertools
from SocketFactory.utilities import utility, gui_utilities
from SocketFactory.gui_alignment.gui_alignment import AlignmentGui

class AlignmentVisGui(QMainWindow):
        
    def __init__(self, size):
        super().__init__()
        self.setWindowTitle('Alignment')
        self.vertical_slack = size.height() * 0.1
        self.horizontal_slack = 0
        self.width = size.width() - self.horizontal_slack
        self.height = size.height() - self.vertical_slack
        self.setGeometry(0, 0, self.width, self.height)
        self.initGUI()

    def initGUI(self):

        self.mdi = QMdiArea()
        self.setCentralWidget(self.mdi) 
        
        mesh_window = QMdiSubWindow()
        mesh_window.setGeometry(int(self.width/4), 0, int(self.width*3/4), self.height)

        frame = Qt.QFrame()
        vl = Qt.QVBoxLayout()
        vtkWidget = QVTKRenderWindowInteractor(frame)
        vl.addWidget(vtkWidget)
        self.ren = vtk.vtkRenderer()
        self.mesh_actor = None
        axes = vtk.vtkAxesActor()
        axes.SetTotalLength(100, 100, 100)
        self.ren.AddActor(axes)
        vtkWidget.GetRenderWindow().AddRenderer(self.ren)
        self.iren = vtkWidget.GetRenderWindow().GetInteractor()
        self.iren.SetInteractorStyle(vtk.vtkInteractorStyleTrackballCamera())
        self.iren.SetRenderWindow(vtkWidget.GetRenderWindow())
        self.ren.ResetCamera()
        frame.setLayout(vl)
        self.iren.Initialize()
        self.iren.Start()
        mesh_window.setWidget(frame)
        self.mdi.addSubWindow(mesh_window)

        # Top-Left subwindow
        alignment_window = QMdiSubWindow()
        alignment_window.setGeometry(0, 0, int(self.width / 4), int(self.height / 2))
        alignment_window.setWidget(AlignmentGui(self))
        self.mdi.addSubWindow(alignment_window)

        # Bottom-Left subwindow
        output_window = QMdiSubWindow()
        output_window.setGeometry(0, int(self.height / 2), int(self.width / 4), self.height / 2)
        output_window.setWidget(self.get_output_window())
        self.mdi.addSubWindow(output_window)

        mesh_window.show()
        alignment_window.show()
        output_window.show()
        self.show()

    def get_output_window(self):
        window = QWidget()
        layout = QGridLayout()
        self.cut_point_label = QLabel("")
        self.anatomical_axis_label = QLabel("")
        self.method_label = QLabel("")
        self.landmarks_label = QLabel("")
        self.origin_label = QLabel("")
        layout.addWidget(QLabel("Cut Point: "), 0, 0)
        layout.addWidget(self.cut_point_label, 0, 1)
        layout.addWidget(QLabel("Longitudinal axis points: "), 1, 0)
        layout.addWidget(self.anatomical_axis_label, 1, 1)
        layout.addWidget(QLabel("Method: "), 2, 0)
        layout.addWidget(self.method_label, 2, 1)
        layout.addWidget(QLabel("Alignment reference landmarks: "), 3, 0)
        layout.addWidget(self.landmarks_label, 3, 1)
        layout.addWidget(QLabel("Origin point: "), 4, 0)
        layout.addWidget(self.origin_label, 4, 1)

        self.output_files = QListWidget()
        self.output_files.itemClicked.connect(self.show_selected_mesh)
        layout.addWidget(self.output_files, 5, 0, 1, 2)
        window.setLayout(layout)
        return window

    def compile_form(self, cut_point, anatomical_axis, method, landmarks, origin):
        self.cut_point_label.setText(cut_point)
        anatomical_axis_string = ""
        for l in anatomical_axis :
            anatomical_axis_string = anatomical_axis_string + str(l) + " " 
        self.anatomical_axis_label.setText(anatomical_axis_string)
        self.method_label.setText(method)
        landmarks_string = ""
        for l in landmarks :
            landmarks_string = landmarks_string + str(l) + " "
        self.landmarks_label.setText(landmarks_string)
        self.origin_label.setText(origin)

    def add_output_meshes(self, meshes_path):
        complete_meshes_path = list(itertools.chain(*meshes_path))
        mesh_names = list(map(lambda x : x.split("/")[-1], complete_meshes_path))
        self.dictionary = dict(zip(mesh_names, complete_meshes_path))
        for m in mesh_names:
            self.output_files.addItem(m)

    @pyqtSlot()
    def show_selected_mesh(self):
        selected_output = self.output_files.currentItem().text()
        mesh_path = self.dictionary[selected_output]
        if (self.mesh_actor is not None):
            self.ren.RemoveActor(self.mesh_actor)

        mesh = utility.read(mesh_path)
        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputData(mesh)
        self.mesh_actor = vtk.vtkActor()
        self.mesh_actor.SetMapper(mapper)
        self.ren.AddActor(self.mesh_actor)
        self.ren.ResetCamera()
        self.iren.ReInitialize()