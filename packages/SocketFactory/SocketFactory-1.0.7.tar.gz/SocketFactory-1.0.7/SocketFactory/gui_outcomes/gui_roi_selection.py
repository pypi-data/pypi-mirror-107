
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import Qt
from PyQt5.QtCore import pyqtSlot
import vtk
import pyvista as pv
import numpy as np
from openpyxl import Workbook
from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
from SocketFactory.utilities import utility, gui_utilities, mesh_to_graph
from SocketFactory.outcomes import region_of_interest

class ROIGui(QMainWindow):
        
    def __init__(self, size):
        super().__init__()
        self.setWindowTitle('Region of interest')
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

        point_picker = vtk.vtkPointPicker()
        self.iren.SetPicker(point_picker)
        self.points = []

        def get_point(obj, ev):
            pos = obj.GetEventPosition()
            newpos = obj.GetPicker().Pick(pos[0], pos[1], 0, obj.GetRenderWindow().GetRenderers().GetFirstRenderer())
            point = obj.GetPicker().GetPickPosition()
            self.points.append(point)
            if (len(self.points) == 3):
                 self.run_btn.setEnabled(True)
            self.sphereActor = gui_utilities.draw_point(point, self.ren, color = [0, 0, 0], radius = 1.5)

        self.iren.AddObserver('RightButtonPressEvent', get_point, 1.0)
        self.iren.Initialize()
        self.iren.Start()
        mesh_window.setWidget(frame)
        self.mdi.addSubWindow(mesh_window)

        # Top-Left subwindow
        info_window = QMdiSubWindow()
        info_window.setGeometry(0, 0, int(self.width / 4), self.height)
        info_window.setWidget(self.selection_widget())
        self.mdi.addSubWindow(info_window)

        mesh_window.show()
        info_window.show()
        self.show()

    def render_mesh(self, mesh_path):

        if (self.mesh_actor is not None):
            self.ren.RemoveActor(self.mesh_actor)

        self.mesh = pv.read(mesh_path)
        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputData(self.mesh)

        self.mesh_actor = vtk.vtkActor()
        self.mesh_actor.SetMapper(mapper)
        
        self.ren.AddActor(self.mesh_actor)
        self.ren.ResetCamera()
        self.iren.ReInitialize()

    def render_trimmed_mesh(self, roi):

        self.ren.RemoveActor(self.mesh_actor)
       
        roiMapper = vtk.vtkPolyDataMapper()
        roiMapper.SetInputData(roi)
    
        roiActor = vtk.vtkActor()
        roiActor.SetMapper(roiMapper)

        self.ren.AddActor(roiActor) # selezione area
        self.ren.ResetCamera()
        self.iren.ReInitialize()

    def visualize_selected_points(self, ids, roi_points):
        vertices = [roi_points.GetPoint(id) for id in ids]

        for v in vertices:
            gui_utilities.draw_point(v, self.ren, color = [0.7,0,0], radius = 0.3)
        self.ren.ResetCamera()
        self.iren.ReInitialize()

    def selection_widget(self):
        widget = QWidget()
        layout = QVBoxLayout()
        info_label1 = QLabel("Select mesh from folder")
        info_label1.setFont(QFont("Arial", 12))
        self.mesh_label = QLabel("")
        mesh_btn = QPushButton("Select mesh")
        mesh_btn.clicked.connect(self.select_mesh)

        info_label2 = QLabel("Select points on mesh (right click)")
        info_label2.setFont(QFont("Arial", 12))
        self.run_btn =  QPushButton("Create ROI")
        self.run_btn.setEnabled(False)
        self.run_btn.clicked.connect(self.process_mesh)

        info_label3 = QLabel("Specify query on vertices quality")
        info_label3.setFont(QFont("Arial", 12))
        self.min_max_label = QLabel("")
        self.query_type = QComboBox()
        self.query_type.addItems(["<", "<=", ">", ">=", "="])
        self.query_value = QDoubleSpinBox()
        self.query_value.setMinimum(-10)
        self.query_btn =  QPushButton("Get query result")
        self.query_btn.setEnabled(False)
        self.query_btn.clicked.connect(self.process_query)
        self.result_label = QLabel("")

        info_label4 = QLabel("Save result")
        info_label4.setFont(QFont("Arial", 12))
        self.save_btn =  QPushButton("Save query result")
        self.save_btn.setEnabled(False)
        self.save_btn.clicked.connect(self.save)

        layout.addWidget(info_label1,)
        layout.addWidget(self.mesh_label)
        layout.addWidget(mesh_btn)
        layout.addStretch()
        layout.addWidget(info_label2)
        layout.addWidget(self.run_btn)
        layout.addStretch()
        layout.addWidget(info_label3)
        layout.addWidget(self.min_max_label)
        layout.addWidget(self.query_type)
        layout.addWidget(self.query_value)
        layout.addWidget(self.query_btn)
        layout.addWidget(self.result_label)
        layout.addStretch()
        layout.addWidget(info_label4)
        layout.addWidget(self.save_btn)
        layout.addStretch()
        widget.setLayout(layout)
        return widget

    def select_mesh(self):
        self.mesh_path, _ = QFileDialog.getOpenFileName(self, 'Open file', filter = "Mesh (*.ply)")
        self.mesh_label.setText(self.mesh_path.split('/')[-1])
        self.render_mesh(self.mesh_path)

    def process_mesh(self):
        self.roi_path = self.mesh_path.split(".")[0] + "_roi.stl"
        roi = region_of_interest.trim_selected_area(self.mesh, self.points, self.roi_path)
        self.render_trimmed_mesh(roi)
       
        # Dictionary: vertex coordinates -> quality
        dict = region_of_interest.create_dictionary(self.mesh_path)
        self.roi_mesh = pv.PolyData(roi)
        self.roi_points = self.roi_mesh.GetPoints()
        self.qualities = [dict[self.roi_points.GetPoint(i)] for i in range(self.roi_points.GetNumberOfPoints())]
        min, max = np.amin(np.array(self.qualities)), np.amax(np.array(self.qualities))
        self.min_max_label.setText("Min value: " + str(round(min, 3)) + ", Max value: " + str(round(max, 3)))
        self.graph = mesh_to_graph.meshQualityGraph(self.roi_mesh, self.qualities)
        self.query_btn.setEnabled(True)
     
    def process_query(self):
        self.ids = mesh_to_graph.query_graph(self.graph, self.query_type.currentText(), float(self.query_value.value()))
        if len(self.ids) > 0:
            self.result_label.setText(str(len(self.ids)) + " correspondence(s) found")
        else:
            self.result_label.setText("No correspondences found")
        self.visualize_selected_points(self.ids, self.roi_points)
        self.save_btn.setEnabled(True)

    def save(self):
        wb = Workbook()
        ws = wb.active
        [ws.append([id, self.mesh.find_closest_point(self.roi_points.GetPoint(id)), self.qualities[id]]) for id in self.ids]
        wb.save(self.mesh_path.split(".")[0] + "_points_of_interest.xlsx")
        