from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import Qt
from PyQt5.QtCore import pyqtSlot
import vtk
from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
from plyfile import PlyData, PlyElement
from SocketFactory.utilities import utility, file_handler, gui_utilities
import numpy as np
import pymeshlab as ml
import os

class CompareMeshVisGUI(QMainWindow):
 
    def __init__(self, size):
        super().__init__()
        self.setWindowTitle('Compare Quality Mapper')
        self.vertical_slack = size.height() * 0.1
        self.horizontal_slack = 0
        self.width = size.width() - self.horizontal_slack
        self.height = size.height() - self.vertical_slack
        self.setGeometry(0, 0, self.width, self.height)
        self.initGUI()
    
    def initGUI(self):
        self.mdi = QMdiArea()
        
        # Main subwindow: meshes visualization
        mesh_window = QMdiSubWindow()
        mesh_window.setGeometry(int(self.width/4), 0, int(self.width*3/4), self.height)
        frame = Qt.QFrame()
        vl = Qt.QVBoxLayout()
        vtkWidget = QVTKRenderWindowInteractor(frame)
        vl.addWidget(vtkWidget)

        self.actor = None
        self.renWin = vtkWidget.GetRenderWindow()
        self.iren = vtkWidget.GetRenderWindow().GetInteractor()
        self.iren.SetInteractorStyle(vtk.vtkInteractorStyleTrackballCamera())
        self.iren.SetRenderWindow(self.renWin)
        frame.setLayout(vl)
        self.iren.Initialize()
        self.iren.Start()
        mesh_window.setWidget(frame)

        # Top-Left subwindow: load and process
        self.load_window = QMdiSubWindow()
        self.load_window.setWindowTitle('Selection Files')
        self.load_window.setGeometry(0, 0, int(self.width/4), int(self.height/2))
        self.load_window.setWidget(self.input_window())

        # Bottom-Left subwindow: quality log
        log_window = QMdiSubWindow()
        log_window.setGeometry(0, int(self.height/2), int(self.width/4), int(self.height/2))
        log_window.setWindowTitle('Set quality mapper parameters')
        log_widget = QWidget()
        log_window.setWidget(log_widget)

        log_layout = QVBoxLayout()
        log_widget.setLayout(log_layout)
        log_layout.addWidget(QLabel('Dataset whiskers'))
        self.whiskers_label = QLabel()
        log_layout.addWidget(self.whiskers_label)
        log_layout.addStretch()

        self.log_min_val = QDoubleSpinBox()
        self.log_min_val.setDecimals(7)
        self.log_min_val.setRange(-50, 50)
        log_layout.addWidget(QLabel('Min Whisker: '))
        log_layout.addWidget(self.log_min_val)

        self.log_max_val= QDoubleSpinBox()
        self.log_max_val.setDecimals(7)
        self.log_min_val.setRange(-50, 50)
        log_layout.addWidget(QLabel('Max Whisker: '))
        log_layout.addWidget(self.log_max_val)

        log_layout.addStretch()

        self.radiobutton_mrgb = QRadioButton("Meshlab RGB Scale")
        self.radiobutton_mrgb.setChecked(True)
        self.radiobutton_rwb = QRadioButton("Red-White-Blue Scale")
        self.radiobutton_rwb.setChecked(False)
        log_layout.addWidget(self.radiobutton_mrgb) 
        log_layout.addWidget(self.radiobutton_rwb)
        
        log_layout.addStretch()
        colorize_btn = QPushButton("Colorize")
        colorize_btn.clicked.connect(self.run)
        log_layout.addWidget(colorize_btn)
        log_layout.addStretch()
        self.mdi.addSubWindow(self.load_window)
        self.mdi.addSubWindow(mesh_window)
        self.mdi.addSubWindow(log_window)
        self.setCentralWidget(self.mdi) 
        mesh_window.show()
        self.load_window.show()
        log_window.show()
        self.show()

    def input_window(self):
        widget = QWidget()
        layout = QVBoxLayout()
        self.mesh_label = QLabel("")
        mesh_btn = QPushButton("Select meshes")
        mesh_btn.clicked.connect(self.select_meshes)
        whiskers_btn = QPushButton("Compute dataset min/max whiskers")
        whiskers_btn.clicked.connect(self.compute_whiskers)
        layout.addWidget(self.mesh_label)
        layout.addWidget(mesh_btn)
        layout.addWidget(whiskers_btn)
        widget.setLayout(layout)
        return widget

    @pyqtSlot()
    def select_meshes(self):
        self.mesh_paths, _ = QFileDialog.getOpenFileNames(self, 'Open file', filter = "Meshes (*.ply)")
        final_label = ''
        for n in self.mesh_paths:
             final_label += n.split("/")[-1] + '\n'
        self.mesh_label.setText(final_label)
        return
    
    def run(self):
        if (self.radiobutton_mrgb.isChecked()) :
            colorscale = 'Meshlab RGB'
            scale = 'rgb'
        if (self.radiobutton_rwb.isChecked()):
            colorscale = 'French RGB'
            scale = 'rwb'

        min = self.log_min_val.value()
        max = self.log_max_val.value() 
        dir_name = file_handler.create_dir(self.mesh_paths[0], 'Quality_mapper_analysis_' + str(min) + '_' + str(max) + '_' + scale)
        new_file = os.path.join(dir_name, dir_name)
        midhandlepos = (0 - min/(max - min))*100
        renderers = self.init_view(len(self.mesh_paths))
        for i, n in enumerate(self.mesh_paths):
            path_out = os.path.join(dir_name, os.path.basename(n))
            self.compute_colorize(n, path_out, colorscale, min, max, midhandlepos)
            self.show_mesh(utility.read(path_out), renderers[i])
              
    def init_view(self, n):
        renderers = [vtk.vtkRenderer() for i in range(n)]
        rows = 2
        columns = n // rows + n % rows
        window_width = 1.0 / columns
        for i, r in enumerate(renderers):
            self.renWin.AddRenderer(r)
            if (i < columns):
                r.SetViewport(i * window_width, 0.5, i * window_width + window_width, 1)
            else :
                r.SetViewport((i - columns) * window_width, 0, (i - columns) * window_width + window_width, 0.5)

            r.ResetCamera()
        return renderers
    
    def compute_whiskers(self):
        min, max = [], []
        for n in self.mesh_paths:
            plydata = PlyData.read(n)
            qualities = plydata['vertex']['quality']
            min_sat, max_sat = utility.calcQuartile(qualities)
            min.append(min_sat)
            max.append(max_sat)

        min, max = np.min(min), np.max(max)

        self.whiskers_label.setText('Min Whisker: ' + str(round(min, 7)) + '\n'  +  'Max Whisker: ' + str(round(max, 7)))
        self.log_min_val.setValue(min)
        self.log_max_val.setValue(max)

    def compute_colorize(self, mesh_path_in, mesh_path_out, colorscale, minsat, maxsat, zeropercentage):
        ms = ml.MeshSet()
        ms.load_new_mesh(mesh_path_in)
        ms.apply_filter('quality_mapper_applier', tfslist = colorscale, midhandlepos = zeropercentage, minqualityval = minsat, maxqualityval = maxsat )
        ms.save_current_mesh(mesh_path_out)

    def show_mesh(self, mesh, ren):
        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputData(mesh)
        actor = vtk.vtkActor()
        actor.SetMapper(mapper)
        ren.AddActor(actor)
        ren.ResetCamera()
        self.iren.ReInitialize()
