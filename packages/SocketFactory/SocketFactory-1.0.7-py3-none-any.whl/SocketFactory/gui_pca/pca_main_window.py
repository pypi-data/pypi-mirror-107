
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import Qt
from PyQt5.QtCore import pyqtSlot
import sys
import vtk
from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
import pyvista as pv
import os.path
from SocketFactory.utilities import utility, file_handler
from SocketFactory.pca.pca import PCAWrapper
from SocketFactory.gui_pca.pca_handling_window import PCAHandlingWindow

class PCAGui(QMainWindow):
        
    def __init__(self, size):
        super().__init__()
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
        mesh_window.setGeometry(int(self.width / 4), 0, int(self.width * 3/4), self.height)

        frame = Qt.QFrame()
        vl = Qt.QVBoxLayout()
        vtkWidget = QVTKRenderWindowInteractor(frame)
        vl.addWidget(vtkWidget)
        self.ren = vtk.vtkRenderer()
        self.mesh_actor = None
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
        pca_input_window = QMdiSubWindow()
        pca_input_window.setGeometry(0, 0, int(self.width / 4), int(self.height / 2))
        pca_input_window.setWidget(self.create_input_window())
        pca_input_window.setWindowTitle("PCA input selection")
        self.mdi.addSubWindow(pca_input_window)

        # Top-Left subwindow
        self.generate_shape_window = QMdiSubWindow()
        self.generate_shape_window.setGeometry(0, int(self.height / 2), int(self.width / 4), int(self.height / 2))
        self.generate_shape_window.setWindowTitle("Shape generation from PCA")
        self.mdi.addSubWindow(self.generate_shape_window)

        mesh_window.show()
        pca_input_window.show()
        self.generate_shape_window.show()
        self.show()

    def create_input_window(self):
        window = QWidget()
        layout = QVBoxLayout()
        self.input_label = QLabel("")
        select_input = QPushButton("Select input meshes")
        self.run_pca_btn = QPushButton("Run pca")
        select_input.clicked.connect(self.select_input)

        layout.addWidget(self.input_label)
        layout.addWidget(select_input)
        layout.addWidget(self.run_pca_btn)
        window.setLayout(layout)
        return window
        
    def show_mesh(self, mesh):
        if (self.mesh_actor is not None):
            self.ren.RemoveActor(self.mesh_actor)

        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputData(mesh)
        self.mesh_actor = vtk.vtkActor()
        self.mesh_actor.SetMapper(mapper)
        self.ren.AddActor(self.mesh_actor)
        self.ren.ResetCamera()
        self.iren.ReInitialize()

    @pyqtSlot()
    def select_input(self):
        self.mesh_paths, _ = QFileDialog.getOpenFileNames(self, 'Open file', filter = "Meshes (*.stl *.ply)")
        final_label = ''
        for n in self.mesh_paths:
             final_label += n.split("/")[-1] + '\n'
        self.input_label.setText(final_label)
        return
  
    @pyqtSlot()
    def run_pca(self, differential = False):
        """
        Run PCA on meshes.
        NB: if differential is True, differential PCA is made.
        """

        if (not differential) :
            self.dir_path = file_handler.create_dir(self.mesh_paths[0], "pca_results")
            self.pca = PCAWrapper(list(map(lambda x : pv.read(x), self.mesh_paths)))
            mean_shape = self.pca.get_mean_shape()
            self.show_mesh(mean_shape)
            utility.write(mean_shape, os.path.join(self.dir_path, "pca_mean_shape.ply"))
            self.generate_shape_window.setWidget(PCAHandlingWindow(self))
        else :
            self.dir_path = file_handler.create_dir(self.mesh_paths[0], "differential_pca_results")
            self.pca = PCAWrapper(list(map(lambda x : pv.read(x), self.mesh_paths)), differential = True)
            self.generate_shape_window.setWidget(PCAHandlingWindow(self, differential = True))