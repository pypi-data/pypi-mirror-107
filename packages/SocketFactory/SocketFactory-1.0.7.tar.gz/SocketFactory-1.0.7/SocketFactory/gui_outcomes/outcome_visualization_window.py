
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import Qt
from PyQt5.QtCore import pyqtSlot
import sys
import vtk
from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
import numpy as np
from SocketFactory.utilities import utility, gui_utilities
from SocketFactory.gui_outcomes.gui_distance import OutcomesDistanceGui

class OutcomeVisGui(QMainWindow):
        
    def __init__(self, size):
        super().__init__()
        self.setWindowTitle('Outcomes')
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
        distance_window = QMdiSubWindow()
        distance_window.setGeometry(0, 0, int(self.width / 4), self.height)
        distance_window.setWidget(OutcomesDistanceGui(self))
        self.mdi.addSubWindow(distance_window)

        mesh_window.show()
        distance_window.show()
        self.show()

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