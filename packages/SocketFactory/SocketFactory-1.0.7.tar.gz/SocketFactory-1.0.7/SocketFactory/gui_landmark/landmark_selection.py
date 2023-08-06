
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import Qt
from PyQt5.QtCore import pyqtSlot
import sys
import numpy as np
import pyvista as pv
from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
import vtk
from SocketFactory.utilities import utility, file_handler, gui_utilities
from SocketFactory.gui_landmark.selection_windows import SelectionModeWindow

class LandMarkSelectionModeGui(QMainWindow):

    def __init__(self, size):
        super().__init__()
        self.setWindowTitle('Landmarks extraction')
        self.window = SelectionModeWindow(self)
        self.vertical_slack = size.height() * 0.1
        self.horizontal_slack = 0
        self.width = size.width() - self.horizontal_slack
        self.height = size.height() - self.vertical_slack
        self.window.show()

    def visualize(self, mesh_path, landmarks_path):
        """
        Creates simple mesh visualization with landmarks.
        """
        mesh = utility.read(mesh_path)
        if (landmarks_path != ""):
            lmk_dict = file_handler.read_points(landmarks_path)
            landmarks_names = lmk_dict.keys()
            landmarks_coordinates = utility.query_dict(lmk_dict, landmarks_names, mesh.GetPoints())
            landmarks = zip(landmarks_names, landmarks_coordinates)
        else:
            landmarks = []
        self.setGeometry(0, 0, self.width, self.height)
        self.setCentralWidget(self.vtk_visualization(mesh, landmarks))

    def vtk_visualization(self, mesh, landmarks):

        frame = Qt.QFrame()
        vl = Qt.QVBoxLayout()
        vtkWidget = QVTKRenderWindowInteractor(frame)
        vl.addWidget(vtkWidget)
        
        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputData(mesh)

        actor = vtk.vtkActor()
        actor.SetMapper(mapper)

        ren = vtk.vtkRenderer()
        ren.AddActor(actor)

        for p in landmarks:
            gui_utilities.draw_point(p[1], ren, color = [0.7, 0, 0], radius = 1.5)
            gui_utilities.add_text(p[0], p[1], ren)

        vtkWidget.GetRenderWindow().AddRenderer(ren)
        iren = vtkWidget.GetRenderWindow().GetInteractor()
        iren.SetInteractorStyle(vtk.vtkInteractorStyleTrackballCamera())
        iren.SetRenderWindow(vtkWidget.GetRenderWindow())

        ren.ResetCamera()
        frame.setLayout(vl)
        self.show()
        iren.Initialize()
        iren.Start()
        return frame

    def select_points(self, single_file_path, file = ""):
        """
        Selects landmarks on single mesh.
        """

        mesh = utility.read(single_file_path)
        if (file == ""):
            self.file = open(single_file_path.split(".")[0] + ".txt", "w+")
            landmarks = []
        else:
            self.file = open(file, "a+")
            lmk_dict = file_handler.read_points(file)
            landmarks_names = lmk_dict.keys()
            landmarks_coordinates = utility.query_dict(lmk_dict, landmarks_names, mesh.GetPoints())
            landmarks = zip(landmarks_names, landmarks_coordinates)

        self.setGeometry(0, 0, self.width, self.height)
        finish_button = QPushButton('Finish', self)
        finish_button.clicked.connect(self.close_all)
        template_frame = Qt.QFrame()
        self.setCentralWidget(template_frame)
        vl = Qt.QVBoxLayout()
        self.vtkWidget = QVTKRenderWindowInteractor(template_frame)
        vl.addWidget(self.vtkWidget)
        vl.addWidget(finish_button)

        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputData(mesh)

        actor = vtk.vtkActor()
        actor.SetMapper(mapper)
        
        actor2 = vtk.vtkActor()
        actor2.SetMapper(mapper)
        actor2.GetProperty().SetRepresentationToWireframe() 

        self.ren = vtk.vtkRenderer()
        self.ren.AddActor(actor2)
        self.ren.AddActor(actor)

        for p in landmarks:
            gui_utilities.draw_point(p[1], self.ren, color = [0, 1, 0])
            # Lables create problems with points selection
            #gui_utilities.add_text(p[0], p[1], self.ren)

        self.vtkWidget.GetRenderWindow().AddRenderer(self.ren)
        self.iren = self.vtkWidget.GetRenderWindow().GetInteractor()

        self.iren.SetInteractorStyle(vtk.vtkInteractorStyleTrackballCamera())
        self.iren.SetRenderWindow(self.vtkWidget.GetRenderWindow())
        point_picker = vtk.vtkPointPicker()
        self.iren.SetPicker(point_picker)

        def get_point(obj, ev):
            pos = obj.GetEventPosition()
            newpos = obj.GetPicker().Pick(pos[0], pos[1], 0, obj.GetRenderWindow().GetRenderers().GetFirstRenderer())
            point = obj.GetPicker().GetPickPosition()
            point_id = obj.GetPicker().GetPointId()
            self.sphereActor = gui_utilities.draw_point(point, self.ren, color = [0.7, 0, 0])
            self.showdialog(point_id, point)

        self.iren.AddObserver('RightButtonPressEvent', get_point, 1.0)
        self.ren.ResetCamera()
        template_frame.setLayout(vl)
        self.show()
        self.iren.Initialize()
        self.iren.Start()

    def showdialog(self, point_id, point):
        """
        Dialog to choose whether to save selected point.
        """
        self.dialog = QDialog()
        formGroupBox = QGroupBox("Save point coordinates")
        layout = QFormLayout()
        self.line_edit = QLineEdit()
        layout.addRow(QLabel("Name:"), self.line_edit)
        formGroupBox.setLayout(layout)
        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)

        buttonBox.accepted.connect(lambda: self.accept(self.line_edit.text(), point_id, point, self.file))
        buttonBox.rejected.connect(self.reject)

        mainLayout = QVBoxLayout()
        self.dialog.setLayout(mainLayout)
        mainLayout.addWidget(formGroupBox)
        mainLayout.addWidget(buttonBox)
        self.dialog.setWindowTitle("Select point")
        self.dialog.exec_()

    @pyqtSlot()
    def accept(self, name, point_id, point, file):
       file_handler.write_point(self.file, point_id, name)
       # Lables create problems with points selection
       #gui_utilities.add_text(name, point, self.ren)
       self.dialog.close()

    @pyqtSlot()
    def reject(self):
       self.ren.RemoveActor(self.sphereActor)
       self.dialog.close()

    @pyqtSlot()
    def close_all(self):
        self.file.close()
        self.close()

    def select_points_from_template(self, file_path, template_path, template_lmk_path):
        """
        Select points in a mesh compared to a template.
        """

        mesh = utility.read(file_path)
        template_mesh = utility.read(template_path)
        lmk_dict = file_handler.read_points(template_lmk_path)
        landmarks_names = lmk_dict.keys()
        landmarks_coordinates = utility.query_dict(lmk_dict, landmarks_names, template_mesh.GetPoints())
        landmarks = list(zip(landmarks_names, landmarks_coordinates))

        self.setGeometry(0, 0, self.width, self.height)
        self.finish_button = QPushButton('Finish', self)
        self.finish_button.clicked.connect(self.close_all)

        self.mdi = QMdiArea()
        self.setCentralWidget(self.mdi)   
        self.template_window(template_mesh)
        self.mesh_window(mesh, file_path)
        self.selection_window(landmarks)

    def template_window(self, template_mesh):
        """
        Creates a window showing template mesh.
        """

        template_window = QMdiSubWindow()
        template_window.setGeometry(0, 0, (int)(self.width/2), (int)(self.height * 3/4))
        self.template_frame = Qt.QFrame()
        template_window.setWidget(self.template_frame)
        self.mdi.addSubWindow(template_window)
        template_window.show()

        vl = Qt.QVBoxLayout()
        self.template_vtkWidget = QVTKRenderWindowInteractor(self.template_frame)
        vl.addWidget(self.template_vtkWidget)

        mapper_template = vtk.vtkPolyDataMapper()
        mapper_template.SetInputData(template_mesh)

        actor_template = vtk.vtkActor()
        actor_template.SetMapper(mapper_template)

        self.template_ren = vtk.vtkRenderer()
        self.template_ren.AddActor(actor_template)

        self.template_vtkWidget.GetRenderWindow().AddRenderer(self.template_ren)
        self.template_iren = self.template_vtkWidget.GetRenderWindow().GetInteractor()
        self.template_iren.SetInteractorStyle(vtk.vtkInteractorStyleTrackballCamera())
        self.template_iren.SetRenderWindow(self.template_vtkWidget.GetRenderWindow())

        self.template_ren.ResetCamera()
        self.template_frame.setLayout(vl)
        self.show()
        self.template_iren.Initialize()
        self.template_iren.Start()

    def mesh_window(self, mesh, file_path):
        """
        Creates window in which select points compared to a template.
        """

        mesh_window = QMdiSubWindow()
        mesh_window.setGeometry((int)(self.width/2), 0, (int)(self.width/2), self.height)
        self.mesh_frame = Qt.QFrame()
        mesh_window.setWidget(self.mesh_frame)
        self.mdi.addSubWindow(mesh_window)
        mesh_window.show()

        vl = Qt.QVBoxLayout()
        self.mesh_vtkWidget = QVTKRenderWindowInteractor(self.mesh_frame)
        vl.addWidget(self.mesh_vtkWidget)

        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputData(mesh)
 
        mesh_actor = vtk.vtkActor()
        mesh_actor.SetMapper(mapper)

        actor2 = vtk.vtkActor()
        actor2.SetMapper(mapper)
        actor2.GetProperty().SetRepresentationToWireframe() 

        self.mesh_ren = vtk.vtkRenderer()
        self.mesh_ren.AddActor(actor2)        
        self.mesh_ren.AddActor(mesh_actor)

        self.mesh_vtkWidget.GetRenderWindow().AddRenderer(self.mesh_ren)
        self.mesh_iren = self.mesh_vtkWidget.GetRenderWindow().GetInteractor()
        self.mesh_iren.SetInteractorStyle(vtk.vtkInteractorStyleTrackballCamera())
        self.mesh_iren.SetRenderWindow(self.mesh_vtkWidget.GetRenderWindow())
        point_picker = vtk.vtkPointPicker()
        self.mesh_iren.SetPicker(point_picker)
        self.point_actor = None
        self.file = open(file_path.split(".")[0] + ".txt", "w+")

        def get_point(obj, ev):
            pos = obj.GetEventPosition()
            newpos = obj.GetPicker().Pick(pos[0], pos[1], 0, obj.GetRenderWindow().GetRenderers().GetFirstRenderer())
            point = obj.GetPicker().GetPickPosition()
            point_id = obj.GetPicker().GetPointId()
            if (self.point_actor is not None):
                self.mesh_ren.RemoveActor(self.point_actor)
            self.point_actor = gui_utilities.draw_point(point, self.mesh_ren, color = [0.7, 0, 0])
            self.take_point(point_id, point)

        self.mesh_iren.AddObserver('RightButtonPressEvent', get_point, 1.0)

        self.mesh_ren.ResetCamera()
        self.mesh_frame.setLayout(vl)

        self.mesh_iren.Initialize()
        self.mesh_iren.Start()
       
    def selection_window(self, points):
        """
        Create a window showing points to be selected.
        """

        self.points = points
        self.point_coordinates = ""
        self.point_id = ""
        self.index = 0
        selection_window = QMdiSubWindow()
        selection_window.setGeometry(0, (int)(self.height * 3/4), (int)(self.width/2), (int)(self.height / 4))
        self.mdi.addSubWindow(selection_window)
        selection_window.show()

        formGroupBox = QGroupBox("Save point coordinates")
        self.layout = QFormLayout()
        self.point_label = QLabel()
        self.point_name = points[self.index][0]
        self.point_name_label = QLabel(self.point_name)
        self.point_name_label.setFont(QFont("Arial", 12))

        self.template_point_actor = gui_utilities.draw_point(points[self.index][1], self.template_ren, color = [0.1, 0, 1], radius = 1.5)
        self.template_text_actor = gui_utilities.add_text(self.point_name, points[self.index][1], self.template_ren)

        self.layout.addRow(self.point_name_label)
        self.layout.addRow(self.point_label)
        formGroupBox.setLayout(self.layout)
        self.buttonBox = QDialogButtonBox(QDialogButtonBox.Save | QDialogButtonBox.Cancel)
        self.layout.addRow(self.buttonBox)
        self.buttonBox.accepted.connect(self.accept_point)
        self.buttonBox.rejected.connect(self.reject_point)

        mainLayout = QVBoxLayout()
        selection_window.setWidget(formGroupBox)
        self.setWindowTitle("Select point")
        
    @pyqtSlot()
    def take_point(self, point_id, point):
        self.point_coordinates = point
        self.point_id = point_id
        self.point_label.setText(str(point))

    @pyqtSlot()
    def accept_point(self):
        file_handler.write_point(self.file, self.point_id, self.point_name)
        self.next_point()

    @pyqtSlot()
    def reject_point(self):
        self.point_coordinates = ""
        self.next_point()

    def next_point(self):
        if (self.point_coordinates != ""):
            gui_utilities.draw_point(self.point_coordinates, self.mesh_ren, color = [0.7, 0, 0])
            # Lables create problems with points selection
            #gui_utilities.add_text(self.point_name, self.point_coordinates, self.mesh_ren)
            self.mesh_iren.ReInitialize()
        if (self.index < len(self.points) - 1):
            self.index += 1
            self.point_label.setText("")
            self.point_name = self.points[self.index][0]
            self.point_name_label.setText(self.point_name)
            self.template_ren.RemoveActor(self.template_point_actor)
            self.template_ren.RemoveActor(self.template_text_actor)
            self.template_point_actor = gui_utilities.draw_point(self.points[self.index][1], self.template_ren, color = [0.1, 0, 1], radius = 1.5)
            self.template_text_actor = gui_utilities.add_text(self.point_name, self.points[self.index][1], self.template_ren)
            self.template_iren.ReInitialize()

        else :
            self.file.close()
            self.close()

    def project_landmarks(self, reference_mesh_path, landmarks_file_path, mesh_path):
        """
        Given a reference mesh, with landmarks, finds closest point on another mesh and creates relative output file.
        """

        ref_mesh = utility.read(reference_mesh_path)
        projection_mesh = pv.read(mesh_path)
        lmk_dict = file_handler.read_points(landmarks_file_path)
        landmarks_names = lmk_dict.keys()
        landmarks_coordinates = utility.query_dict(lmk_dict, landmarks_names, ref_mesh.GetPoints())
        landmarks = zip(landmarks_names, landmarks_coordinates)

        file_path = mesh_path.split(".")[0] + ".txt"
        file = open(file_path, "w+")
        for name, coordinates in landmarks:
            point_id = projection_mesh.find_closest_point(coordinates)
            file_handler.write_point(file, point_id, name)
        file.close()
        self.visualize(mesh_path, file_path)