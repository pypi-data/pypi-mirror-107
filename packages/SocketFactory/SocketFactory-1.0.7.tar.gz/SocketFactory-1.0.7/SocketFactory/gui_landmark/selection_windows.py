
from PyQt5.QtWidgets import *
from PyQt5 import Qt
from PyQt5.QtCore import pyqtSlot

class SelectionModeWindow(QWidget):
    """
    Window to select landmarks on mesh.
    """

    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.initGUI()

    def initGUI(self):
        self.resize(1000, 200)
        self.setWindowTitle('Landmarks extraction')
        grid = QGridLayout()
        grid.setSpacing(10)
        self.setLayout(grid)
        grid.addWidget(self.mesh_visualization(), 0, 0)
        grid.addWidget(self.single_file_selection(), 0, 1)
        grid.addWidget(self.multiple_file_selection(), 0, 2)
        grid.addWidget(self.projected_landmarks(), 0, 3)

    def mesh_visualization(self):

        self.landmarks_path = ""
        groupBox = QGroupBox("Mesh visualization")
        self.vis_file_label = QLabel('', self)
        vis_file_btn = QPushButton('Load mesh')
        self.vis_landmarks_label = QLabel('', self)
        vis_landmarks_btn = QPushButton('Load landmarks')
        vis_btn = QPushButton('Visualize', self)
        vis_btn.setStyleSheet("background-color : orange")

        vis_file_btn.clicked.connect(lambda: self.choose_file(self.vis_file_label))
        vis_landmarks_btn.clicked.connect(lambda: self.choose_points_file(self.vis_landmarks_label))
        vis_btn.clicked.connect(self.visualize)

        vbox = QVBoxLayout()
        vbox.addWidget(self.vis_file_label)
        vbox.addWidget(vis_file_btn)
        vbox.addWidget(self.vis_landmarks_label)
        vbox.addWidget(vis_landmarks_btn)
        vbox.addWidget(vis_btn)

        groupBox.setLayout(vbox)
        return groupBox

    def single_file_selection(self):
        groupBox = QGroupBox("Landmarks selection")
        single_file_btn = QPushButton('Load mesh')
        run_single_file_btn = QPushButton('Select landmarks', self)
        run_single_file_btn.clicked.connect(self.run_single)
        run_single_file_btn.setStyleSheet("background-color : lightblue")
        self.single_file_label = QLabel('', self)
        single_file_btn.clicked.connect(lambda: self.choose_file(self.single_file_label))

        existing_lmk_btn = QPushButton('Load existing landmarks file')
        self.existing_lmk_label = QLabel('', self)
        existing_lmk_btn.clicked.connect(lambda: self.choose_points_file(self.existing_lmk_label))

        vbox = QVBoxLayout()
        vbox.addWidget(self.single_file_label)
        vbox.addWidget(single_file_btn)
        vbox.addWidget(self.existing_lmk_label)
        vbox.addWidget(existing_lmk_btn)
        vbox.addWidget(run_single_file_btn)
        groupBox.setLayout(vbox)

        return groupBox

    def multiple_file_selection(self):
        groupBox = QGroupBox("Landmarks selection with template")

        template_btn = QPushButton('Load template mesh', self)
        file_btn = QPushButton('Load mesh', self)
        landmarks_btn = QPushButton('Load landamarks', self)

        self.template_file_label = QLabel('', self)
        self.file_label = QLabel('', self)
        self.landmarks_label = QLabel('', self)
        run_multiple_file_btn = QPushButton('Select landmarks', self)
        run_multiple_file_btn.setStyleSheet("background-color : lightblue")

        template_btn.clicked.connect(self.choose_template_file)
        landmarks_btn.clicked.connect(lambda: self.choose_points_file(self.landmarks_label))
        file_btn.clicked.connect(lambda: self.choose_file(self.file_label))
        run_multiple_file_btn.clicked.connect(self.run_multiple)

        vbox = QVBoxLayout()
        vbox.addWidget(self.template_file_label)
        vbox.addWidget(template_btn)
        vbox.addWidget(self.landmarks_label)
        vbox.addWidget(landmarks_btn)
        vbox.addWidget(self.file_label)
        vbox.addWidget(file_btn)
        vbox.addWidget(run_multiple_file_btn)
        groupBox.setLayout(vbox)
        return groupBox

    def projected_landmarks(self):
        groupBox = QGroupBox("Landmarks by projection")

        reference_btn = QPushButton('Load reference mesh', self)
        landmarks_btn = QPushButton('Load reference landamarks', self)
        mesh_btn = QPushButton('Load mesh', self)
        self.reference_file_label = QLabel('', self)
        self.proj_landmarks_label = QLabel('', self)
        self.mesh_label = QLabel('', self)
        run_projection_btn = QPushButton('Project and Visualize', self)
        run_projection_btn.setStyleSheet("background-color : lightblue")

        reference_btn.clicked.connect(self.choose_reference_mesh)
        landmarks_btn.clicked.connect(lambda: self.choose_points_file(self.proj_landmarks_label))
        mesh_btn.clicked.connect(lambda: self.choose_file(self.mesh_label))
        run_projection_btn.clicked.connect(self.run_projection)

        vbox = QVBoxLayout()
        vbox.addWidget(self.reference_file_label)
        vbox.addWidget(reference_btn)
        vbox.addWidget(self.proj_landmarks_label)
        vbox.addWidget(landmarks_btn)
        vbox.addWidget(self.mesh_label)
        vbox.addWidget(mesh_btn)
        vbox.addWidget(run_projection_btn)
        groupBox.setLayout(vbox)
        return groupBox

    @pyqtSlot()
    def choose_file(self, label):
        self.single_file_path, _ = QFileDialog.getOpenFileName(self, 'Open file', filter = "Meshes (*.stl *.ply)")
        label.setText(self.single_file_path.split("/")[-1])
        return

    @pyqtSlot()
    def choose_template_file(self):
        self.template_file_path, _ = QFileDialog.getOpenFileName(self, 'Open file', filter = "Meshes (*.stl *.ply)")
        self.template_file_label.setText(self.template_file_path.split("/")[-1])
        return

    @pyqtSlot()
    def choose_points_file(self, label):
        self.landmarks_path, _ = QFileDialog.getOpenFileName(self, 'Open file', filter = "Text (*.txt)")
        label.setText(self.landmarks_path.split("/")[-1])
        return

    @pyqtSlot()
    def visualize(self):
        self.close()
        self.parent.visualize(self.single_file_path, self.landmarks_path)

    @pyqtSlot()
    def choose_reference_mesh(self):
        self.reference_mesh_path, _ = QFileDialog.getOpenFileName(self, 'Open file', filter = "Meshes (*.stl *.ply)")
        self.reference_file_label.setText(self.reference_mesh_path.split("/")[-1])
        return
        
    @pyqtSlot()
    def run_single(self):
        self.close()
        if (self.existing_lmk_label.text() == ''):
            self.parent.select_points(self.single_file_path)
        else :
            self.parent.select_points(self.single_file_path, self.landmarks_path)

    @pyqtSlot()
    def run_multiple(self):
        self.close()
        self.parent.select_points_from_template(self.single_file_path, self.template_file_path, self.landmarks_path)

    @pyqtSlot()
    def run_projection(self):
        self.close()
        self.parent.project_landmarks(self.reference_mesh_path, self.landmarks_path, self.single_file_path)