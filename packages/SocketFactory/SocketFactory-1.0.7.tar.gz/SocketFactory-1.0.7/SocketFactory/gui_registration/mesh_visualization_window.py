
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import Qt
from PyQt5.QtCore import pyqtSlot
import numpy as np
from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
import vtk
from SocketFactory.utilities import utility, gui_utilities
from SocketFactory.gui_registration.registration_main_window import RegistrationGui
from SocketFactory.gui_registration.register_other_meshes_window import OtherMeshesRegistrationGui

class MeshRegistrationGui(QMainWindow):

    def __init__(self, size):
        super().__init__()
        self.setWindowTitle('Mesh Registration')
        self.vertical_slack = size.height() * 0.1
        self.horizontal_slack = 0
        self.width = size.width() - self.horizontal_slack
        self.height = size.height() - self.vertical_slack
        self.setGeometry(0, 0, self.width, self.height)
        self.static_color = (0.67, 0.71, 0.8)
        self.moving_color = (0.94, 0.7, 0.48)
        self.registration_widget = RegistrationGui(self)
        self.init()

    def init(self):
        self.mdi = QMdiArea()
        
        # Main subwindow: meshes visualization
        mesh_window = QMdiSubWindow()
        mesh_window.setGeometry(int(self.width/3), 0, int(self.width*2/3), self.height)
        frame = Qt.QFrame()
        vl = Qt.QVBoxLayout()
        vtkWidget = QVTKRenderWindowInteractor(frame)
        vl.addWidget(vtkWidget)
        self.ren = vtk.vtkRenderer()
        self.static_actor = None
        self.moving_actor = None
        vtkWidget.GetRenderWindow().AddRenderer(self.ren)
        self.iren = vtkWidget.GetRenderWindow().GetInteractor()
        self.iren.SetInteractorStyle(vtk.vtkInteractorStyleTrackballCamera())
        self.iren.SetRenderWindow(vtkWidget.GetRenderWindow())
        self.ren.ResetCamera()
        frame.setLayout(vl)
        self.iren.Initialize()
        self.iren.Start()
        mesh_window.setWidget(frame)

        # Top-Left subwindow: registration methods and parameters
        self.reg_window = QMdiSubWindow()
        self.reg_window.setGeometry(0, 0, int(self.width/3), int(self.height/2))
        self.reg_window.setWidget(self.registration_widget)

        # Bottom-Left subwindow: registration log
        log_window = QMdiSubWindow()
        log_window.setGeometry(0, int(self.height/2), int(self.width/3), int(self.height/2))
        log_widget = QWidget()
        log_window.setWidget(log_widget)
        log_layout = QVBoxLayout()
        log_widget.setLayout(log_layout)
        self.log_list = QListWidget()
        log_layout.addWidget(self.log_list)
        log_window.setWindowTitle('Registration log')

        self.mdi.addSubWindow(self.reg_window)
        self.mdi.addSubWindow(mesh_window)
        self.mdi.addSubWindow(log_window)
        self.setCentralWidget(self.mdi) 
        mesh_window.show()
        self.reg_window.show()
        log_window.show()
        self.show()

    def set_static_mesh(self, mesh):

        if (self.static_actor is not None):
            self.ren.RemoveActor(self.static_actor)

        self.static_mesh = mesh
        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputData(self.static_mesh)
        self.static_actor = vtk.vtkActor()
        self.static_actor.SetMapper(mapper)
        self.static_actor.GetProperty().SetColor(self.static_color)
        self.ren.AddActor(self.static_actor)
        self.ren.ResetCamera()
        self.iren.ReInitialize()

    def set_moving_mesh(self, mesh):

        if (self.moving_actor is not None):
            self.ren.RemoveActor(self.moving_actor)

        self.moving_mesh = mesh
        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputData(self.moving_mesh)
        self.moving_actor = vtk.vtkActor()
        self.moving_actor.SetMapper(mapper)
        self.moving_actor.GetProperty().SetColor(self.moving_color)
        self.ren.AddActor(self.moving_actor)
        self.ren.ResetCamera()
        self.iren.ReInitialize()

    def add_mesh(self, mesh_path):
        mesh = utility.read(mesh_path)
        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputData(mesh)
        actor = vtk.vtkActor()
        actor.SetMapper(mapper)
        actor.GetProperty().SetColor(gui_utilities.generate_random_color())
        self.ren.AddActor(actor)
        self.ren.ResetCamera()
        self.iren.ReInitialize()

    def add_log(self, log):
        self.log_list.addItem(log)

    def add_other_mesh_application_window(self, output_matrices):
        self.mdi.removeSubWindow(self.reg_window)
        other_mesh_window = QMdiSubWindow()
        other_mesh_window.setGeometry(0, 0, int(self.width/3), int(self.height/2))
        self.other_mesh_registration_widget = OtherMeshesRegistrationGui(self, output_matrices)
        other_mesh_window.setWidget(self.other_mesh_registration_widget)
        self.mdi.addSubWindow(other_mesh_window)
        other_mesh_window.show()
