
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, pyqtSlot
from PyQt5.QtGui import *
from SocketFactory.utilities import utility, file_handler, gui_utilities
from SocketFactory.outcomes import geodesic_path
from openpyxl import Workbook
import pyvista as pv
import vtk
import os

class GeodesicGui(QMainWindow):
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Geodesic Distance')
        self.initGUI()
    
    def initGUI(self):

        self.width = 800
        self.height = 400
        self.resize(self.width, self.height)
        self.main_widget = QWidget()
        self.setCentralWidget(self.main_widget)
        grid = QGridLayout()
        grid.setSpacing(10)
        grid.setColumnStretch(0, 1)
        grid.setColumnStretch(1, 2)
        self.main_widget.setLayout(grid)
        grid.addWidget(self.mesh_selection(), 0, 0)
        grid.addWidget(self.set_parameters(), 0, 1)
        self.show()

    def mesh_selection(self):
        groupBox = QGroupBox("Files selection")
        self.mesh_paths = []
        self.mesh_label = QLabel("", self)
        mesh_btn = QPushButton("Load mesh files")
        mesh_btn.clicked.connect(self.choose_meshes)

        self.landmark_paths = []
        self.landmark_label = QLabel("", self)
        landmark_btn = QPushButton("Load landmark files")
        landmark_btn.clicked.connect(self.choose_landmarks)

        vbox = QVBoxLayout()
        vbox.addWidget(self.mesh_label)
        vbox.addWidget(mesh_btn)
        vbox.addWidget(self.landmark_label)        
        vbox.addWidget(landmark_btn)
        groupBox.setLayout(vbox)
        return groupBox

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
    def choose_landmarks(self) :
        self.landmark_paths, _ = QFileDialog.getOpenFileNames(self, 'Open file', filter = "Text (*.txt)")
        self.landmark_paths.sort()
        final_label = ''
        for n in self.landmark_paths:
            final_label += n.split("/")[-1] + '\n'
        self.landmark_label.setText(final_label)
        return

    def set_parameters(self):
        groupBox = QGroupBox("Parameters selection")
        vbox = QVBoxLayout()

        self.radiobutton_all_lmk = QRadioButton("Distance of all landmarks from apex mode")
        self.radiobutton_all_lmk.setChecked(True)
        self.radiobutton_two_lmk = QRadioButton("Distance between two landmarks mode")
        self.radiobutton_two_lmk.setChecked(False)


        grid_layout1 = QGridLayout()
        start_point_label1 = QLabel("Starting point: ")
        self.start_point1 = QLineEdit()
        grid_layout1.addWidget(start_point_label1, 0, 0)
        grid_layout1.addWidget(self.start_point1, 0, 1)
        end_point_label1 = QLabel("Ending point: ")
        self.end_point1 = QLineEdit()
        grid_layout1.addWidget(end_point_label1, 1, 0)
        grid_layout1.addWidget(self.end_point1, 1, 1)

        point_percentage_label1 = QLabel("Find point along geodesic path at: ")
        self.point_percentage = QSpinBox()
        self.point_percentage.setRange(0, 100)
        self.point_percentage.setSingleStep(5)
        self.point_percentage.setSuffix(' %')
        grid_layout1.addWidget(point_percentage_label1, 2, 0)
        grid_layout1.addWidget(self.point_percentage, 2, 1)
   

        run_btn = QPushButton("Compute geodesic path")
        run_btn.setStyleSheet("background-color : lightpink")
        run_btn.clicked.connect(self.run)

        vbox.addWidget(self.radiobutton_all_lmk)
        vbox.addWidget(self.radiobutton_two_lmk)
        vbox.addLayout(grid_layout1)
        vbox.addWidget(run_btn)
        groupBox.setLayout(vbox)
        return groupBox

    def handle_landmarks(self, m_path, l_path):
        mesh = pv.read(m_path)
        lmk_dict = file_handler.read_points(l_path)
        return mesh, lmk_dict
    
    def handle_starting_ending_point(self, m_path, l_path, starting_point, ending_point):
        mesh, lmk_dict = self.handle_landmarks(m_path, l_path)
        starting_point_index = lmk_dict[starting_point]
        ending_point_index = lmk_dict[ending_point]
        return mesh, int(starting_point_index), int(ending_point_index)

    @pyqtSlot()
    def run(self):
        self.close()
        # Init output measures file
        wb = Workbook()
        ws = wb.active

        if (self.radiobutton_all_lmk.isChecked()) :
            ending_point_name = 'a'
            for m_path, l_path in zip(self.mesh_paths, self.landmark_paths) :
                
                mesh, lmk_dict = self.handle_landmarks(m_path, l_path)
                ws, main_path, paths = geodesic_path.compute_all_lmk_paths_distances(mesh, lmk_dict, m_path, ending_point_name, ws)
                gui_utilities.render_geodesic(paths, mesh)

        elif (self.radiobutton_two_lmk.isChecked()) :
            starting_point_name = self.start_point1.text().lower()
            ending_point_name =  self.end_point1.text().lower()
            percentage = self.point_percentage.value() / 100
           
            for m_path, l_path in zip(self.mesh_paths, self.landmark_paths) :

                mesh, starting_point_index, ending_point_index = self.handle_starting_ending_point(m_path, l_path, starting_point_name, ending_point_name)

                main_path, dir_path, file_name = file_handler.create_dir_by_filename(m_path, ' geodesic paths')
                points_name = starting_point_name + '_' + ending_point_name
                
                file = os.path.join(dir_path, points_name + '.ply')
                path, distance = geodesic_path.compute_path_distance(mesh, starting_point_index, ending_point_index, file)
                df_row = [file_name]
                df_row.extend([points_name, distance])

                if (percentage != 0):
                    first_distance = distance * percentage
                    second_distance = distance - first_distance
                    point = geodesic_path.find_point_geodesic_path(path, distance, percentage)
                    point_id = mesh.find_closest_point(point)
                    gui_utilities.render_geodesic([path], mesh, point)
                    df_row.extend([percentage, point_id, first_distance, second_distance])
                else:
                    gui_utilities.render_geodesic([path], mesh)

                ws.append(df_row)

        wb.save(os.path.join(main_path, "Measures_geodesic.xlsx"))
                


                                                    