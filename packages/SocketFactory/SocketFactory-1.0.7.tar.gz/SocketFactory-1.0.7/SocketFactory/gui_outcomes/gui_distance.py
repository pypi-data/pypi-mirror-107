from PyQt5.QtWidgets import *
from PyQt5 import Qt, QtCore
from PyQt5.QtCore import pyqtSlot
from vtk.util import numpy_support
from SocketFactory.utilities import file_handler, utility
from SocketFactory.outcomes import distance
import pyvista as pv
import os.path
from SocketFactory.tests.common import rmse
import numpy as np

class OutcomesDistanceGui(QWidget):

    def __init__(self, parent):                                                        
        super().__init__()
        self.parent = parent
        self.setWindowTitle('Outcomes Interface')
        self.re_name = "RE/INAIL distance"
        self.vv_dist_name = "Vertex-vertex distance"
        self.meshlab_distance_name = "Meshlab distance"
        self.snae_name = "Snae"
        self.normal_similarity_name = "Normal Similarity"
        self.pca_distance = "PCA preparation vectors"
        self.initGUI()

    def initGUI(self):

        grid = QGridLayout()
        grid.setSpacing(10)
        self.setLayout(grid)
        grid.addWidget(self.file_selection(), 0, 0)
        grid.addWidget(self.distance_mode_selection(), 1, 0)
        grid.addWidget(self.mesh_show_selection(), 2, 0)
        self.show()

    def file_selection(self):
        groupBox = QGroupBox("File selection")
        
        ref_file_btn = QPushButton('Load reference mesh',self)
        ref_file_btn.clicked.connect(self.choose_ref_file)
        self.ref_file_label = QLabel('', self)

        mea_file_btn = QPushButton('Load measured mesh',self)
        mea_file_btn.clicked.connect(self.choose_mea_file)
        self.mea_file_label = QLabel('', self)

        rmse_btn = QPushButton("Compute RMSE")
        rmse_btn.clicked.connect(self.compute_rmse)
        self.rmse_label = QLabel('', self)
        self.rmse_label.setTextInteractionFlags(QtCore.Qt.TextSelectableByMouse)

        vbox = QVBoxLayout()
        vbox.addWidget(self.ref_file_label)
        vbox.addWidget(ref_file_btn)
        vbox.addWidget(self.mea_file_label)        
        vbox.addWidget(mea_file_btn)
        vbox.addWidget(self.rmse_label)
        vbox.addWidget(rmse_btn)
        groupBox.setLayout(vbox)
        return groupBox

    def distance_mode_selection(self):
        groupBox = QGroupBox("Distance mode selection")

        run_btn = QPushButton('Compute distance and create files', self)
        run_btn.clicked.connect(lambda: self.run(self.ref_file_path, self.mea_file_path))
        run_btn.setStyleSheet("background-color : orange")
        
        self.checkBox_re_dist = QCheckBox(self)
        self.checkBox_re_dist.setText(self.re_name)

        self.checkBox_vv_dist = QCheckBox(self)
        self.checkBox_vv_dist.setText(self.vv_dist_name)
        
        self.checkBox_ms_dist = QCheckBox(self)
        self.checkBox_ms_dist.setText(self.meshlab_distance_name)

        self.checkBox_snae = QCheckBox(self)
        self.checkBox_snae.setText(self.snae_name)

        self.checkBox_normal_similarity = QCheckBox(self)
        self.checkBox_normal_similarity.setText(self.normal_similarity_name)

        self.checkBox_pca_dist = QCheckBox(self)
        self.checkBox_pca_dist.setText(self.pca_distance)

        vbox = QVBoxLayout()
        vbox.addWidget(self.checkBox_re_dist)
        vbox.addWidget(self.checkBox_vv_dist)
        vbox.addWidget(self.checkBox_ms_dist)
        vbox.addWidget(self.checkBox_snae)
        vbox.addWidget(self.checkBox_normal_similarity)
        vbox.addWidget(self.checkBox_pca_dist)
        vbox.addWidget(run_btn)
        groupBox.setLayout(vbox)
        return groupBox

    @pyqtSlot()
    def choose_ref_file(self):
        self.ref_file_path, _ = QFileDialog.getOpenFileName(self, 'Open file', filter = "Meshes (*.stl *.ply)")
        self.ref_file_label.setText(self.ref_file_path.split("/")[-1])
        return

    @pyqtSlot()
    def choose_mea_file(self):
        self.mea_file_path, _ = QFileDialog.getOpenFileName(self, 'Open file', filter = "Meshes (*.stl *.ply)")
        self.mea_file_label.setText(self.mea_file_path.split("/")[-1])
        return

    def compute_rmse(self):
        ref_mesh = utility.read(self.ref_file_path)
        mea_mesh = utility.read(self.mea_file_path)
        rmse_value = rmse(utility.get_vertices(ref_mesh), utility.get_vertices(mea_mesh))
        self.rmse_label.setText(str(rmse_value))

    def mesh_show_selection(self):
        groupBox = QGroupBox("Mesh selection")
        self.output_list = QListWidget()
        self.output_list.itemClicked.connect(self.show_selected_mesh)
        vbox = QVBoxLayout()
        vbox.addWidget(self.output_list)
        groupBox.setLayout(vbox)
        return groupBox

    @pyqtSlot()
    def show_selected_mesh(self):
        selected_output = self.output_list.currentItem().text()
        if (selected_output == self.re_name) :
            self.parent.show_mesh(utility.read(self.re_ply_path))
        elif (selected_output == self.vv_dist_name):
            self.parent.show_mesh(utility.read(self.vv_ply_path))
        elif (selected_output == self.meshlab_distance_name):
            self.parent.show_mesh(utility.read(self.ms_ply_path))
        elif (selected_output == self.snae_name):
            self.parent.show_mesh(utility.read(self.snae_ply_path))
        elif (selected_output == self.normal_similarity_name):
            self.parent.show_mesh(utility.read(self.normal_similarity_ply_path))
        
    def run(self, path_ref, path_mea):

        ref_pv = pv.read(path_ref)
        mea_pv = pv.read(path_mea)
        
        ref_vert = utility.get_vertices(ref_pv)
        mea_vert = utility.get_vertices(mea_pv)

        ref_pv.compute_normals()
        ref_norm = ref_pv.point_normals

        mea_pv.compute_normals()
        mea_norm = mea_pv.point_normals
        mea_faces = file_handler.getFaces(mea_pv.faces)
        main_path, dir_name, file_name = file_handler.create_dir_by_filename(path_mea, '_outcomes')
      
        if (self.checkBox_vv_dist.isChecked()):
            values = distance.compute_vv_distance(ref_vert, mea_vert, ref_norm)
            self.vv_ply_path = os.path.join(dir_name, file_name + "_vv_dist.ply")
            min_sat, max_sat = utility.calcQuartile(values)
            ply_comment = 'Vertex-Vertex distance and color map range from ' + str(np.around(min_sat, 4)) + ' to ' + str(np.around(max_sat, 4))
            file_handler.create_ply_with_colour(mea_vert, mea_faces, values, 'vv', self.vv_ply_path, min_sat, max_sat, comment = ply_comment)
            self.output_list.addItem(self.vv_dist_name)
            file_handler.convertPlyToXlsx(self.vv_ply_path)

        if (self.checkBox_ms_dist.isChecked()):
            self.ms_ply_path = os.path.join(dir_name, file_name + "_meshlab_dist.ply")
            distance.compute_ms_distance(path_ref, path_mea, self.ms_ply_path)
            distance.compute_colorize(self.ms_ply_path, self.ms_ply_path)
            self.output_list.addItem(self.meshlab_distance_name)
            file_handler.convertPlyToXlsx(self.ms_ply_path)

        if (self.checkBox_re_dist.isChecked()):
            ref_vert, ref_norm = distance.find_closest_points(ref_vert, mea_vert, ref_norm)
            values = distance.compute_re_distance(ref_vert, mea_vert, ref_norm)
            min_sat, max_sat = utility.calcQuartile(values)
            self.re_ply_path = os.path.join(dir_name, file_name + "_re_dist.ply")
            ply_comment = self.re_name + ' '+ 'color map range from ' + str(np.around(min_sat, 4)) + ' to ' + str(np.around(max_sat, 4))
            file_handler.create_ply_with_colour(mea_vert, mea_faces, values, 're', self.re_ply_path, min_sat, max_sat, comment = ply_comment)
            mesh = pv.read(self.re_ply_path)
            self.output_list.addItem(self.re_name)
            file_handler.convertPlyToXlsx(self.re_ply_path)
            
        if (self.checkBox_normal_similarity.isChecked()):
            ref_vert, ref_norm = distance.find_closest_points(ref_vert, mea_vert, ref_norm)
            values = distance.compute_normal_similarity(ref_norm, mea_norm)
            _, max_sat = utility.calcQuartile(values)
            min_sat = 0
            self.normal_similarity_ply_path = os.path.join(dir_name, file_name + "_normal_similarity.ply")
            ply_comment = 'Normal Similarity (atanh) and colour map range from ' + str(min_sat) + ' to ' + str(np.around(max_sat, 4))
            file_handler.create_ply_with_colour(mea_vert, mea_faces, values, 'normal_similarity', self.normal_similarity_ply_path, min_sat, max_sat, comment = ply_comment)
            self.output_list.addItem(self.normal_similarity_name)
            file_handler.convertPlyToXlsx(self.normal_similarity_ply_path)
            
        if (self.checkBox_snae.isChecked()):
            ref_vert, ref_norm = distance.find_closest_points(ref_vert, mea_vert, ref_norm)
            values = distance.compute_snae(ref_norm, mea_norm)
            self.snae_ply_path = os.path.join(dir_name, file_name + '_snae.ply')
            _, max_sat =  utility.calcQuartile(values)
            min_sat = 0
            ply_comment = 'Snae (arccos - degrees) and colour map range from ' + str(min_sat) + ' to ' + str(np.around(max_sat, 4))
            file_handler.create_ply_with_colour(mea_vert, mea_faces, values, 'snae', self.snae_ply_path, min_sat, max_sat, comment = ply_comment)
            self.output_list.addItem(self.snae_name)
            file_handler.convertPlyToXlsx(self.snae_ply_path)
            
        if (self.checkBox_pca_dist.isChecked()):
            values = mea_vert - ref_vert
            ply_path = os.path.join(dir_name, file_name + '_pca.ply')
            utility.write(pv.PolyData(values), ply_path)