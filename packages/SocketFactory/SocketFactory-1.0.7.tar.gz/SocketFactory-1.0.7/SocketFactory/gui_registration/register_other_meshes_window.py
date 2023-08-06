
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import vtk
from SocketFactory.utilities import utility
from SocketFactory.registration import registration_methods

class OtherMeshesRegistrationGui(QWidget):

    def __init__(self, parent, transform):
        super().__init__()
        self.parent = parent
        self.setWindowTitle('Apply registration to other meshes')

        self.transformFilter = vtk.vtkTransformPolyDataFilter()
        self.transformFilter.SetTransform(transform)
        self.init()

    def init(self):
        grid = QGridLayout()

        self.meshes_label = QLabel("")
        meshes_btn = QPushButton("Select meshes")
        meshes_btn.clicked.connect(self.select_meshes)

        run_btn = QPushButton("Apply transformation")
        run_btn.clicked.connect(self.apply_transformation)

        grid.addWidget(self.meshes_label, 0, 0)
        grid.addWidget(meshes_btn, 2, 0)
        grid.addWidget(run_btn, 3, 0)
        self.setLayout(grid)

    def select_meshes(self):
        self.meshes_paths, _ = QFileDialog.getOpenFileNames(self, 'Open file', filter = "Meshes (*.stl *.ply)")
        final_label = ''
        for n in self.meshes_paths:
             final_label += n.split("/")[-1] + '\n'
        self.meshes_label.setText(final_label)

    def apply_transformation(self):
        meshes = list(map(utility.read, self.meshes_paths))

        for (mesh, name) in zip(meshes, list(map(lambda x : x.split(".")[0], self.meshes_paths))) :
            self.transformFilter.SetInputData(mesh)
            self.transformFilter.Update()
            output_mesh = self.transformFilter.GetOutput()
            output_file = name + "_reg.ply"
            utility.write(output_mesh, output_file)
            self.parent.add_mesh(output_file)

        self.meshes_label.setText("")