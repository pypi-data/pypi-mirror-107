from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import vtk
import numpy as np
import os.path
from SocketFactory.utilities import utility, file_handler
from collections import OrderedDict 
from SocketFactory.registration import registration_methods as registration
from SocketFactory.gui_registration.parameters_dialog import ParametersDialog

class RegistrationGui(QWidget):

    def __init__(self, parent):

        super().__init__()
        self.parent = parent
        self.landmarks_name = "Landmark"
        self.rigid_name = "ICP_rigid"
        self.similarity_name = "ICP_similarity"
        self.affine_name = "ICP_affine"
        self.sanders_name = "Sanders"
        self.tps_name = "TPS"
        self.procrustes_name = "Procrustes"
        self.registrations = [self.landmarks_name, self.rigid_name, self.similarity_name, self.affine_name, self.sanders_name, 
                              self.tps_name, self.procrustes_name]
        self.setWindowTitle('Registration')
        self.initGUI()
        self.next_button.clicked.connect(self.next_page)
        self.insert_first_page()

    def initGUI(self):
        self.next_button = QPushButton('Continue')
        self.stacked_widget = QStackedWidget()
        self.hbox = QHBoxLayout()
        self.hbox.addWidget(self.next_button)
        vbox = QVBoxLayout()
        vbox.addWidget(self.stacked_widget)
        vbox.addLayout(self.hbox)
        self.setLayout(vbox)

    def change_btn(self):
        self.hbox.removeWidget(self.next_button)
        self.run_button = QPushButton()
        self.run_button.setText("Run registration")
        self.run_button.clicked.connect(self.run_registration)
        self.hbox.addWidget(self.run_button)

    def insert_first_page(self, index=-1):
        first_page = QWidget()
        self.static_label = QLabel("")
        static_btn = QPushButton("Select static mesh")
        static_btn.clicked.connect(self.choose_static_mesh)
        self.moving_label = QLabel("")
        moving_btn = QPushButton("Select moving mesh")
        moving_btn.clicked.connect(self.choose_moving_mesh)
        
        # Dictionary: registration name -> relative checkbox
        self.checkboxes = {}

        vbox = QVBoxLayout()
        vbox.addStretch(1)
        vbox.addWidget(self.static_label)
        vbox.addWidget(static_btn)
        vbox.addWidget(self.moving_label)
        vbox.addWidget(moving_btn)

        for r in self.registrations:
            checkBox = QCheckBox(self)
            checkBox.setText(r)
            self.checkboxes[r] = checkBox
            vbox.addWidget(checkBox)

        first_page.setLayout(vbox)
        self.stacked_widget.insertWidget(index, first_page)
   
    @pyqtSlot()
    def choose_static_mesh(self):
        self.static_path, _ = QFileDialog.getOpenFileName(self, 'Open file', filter = "Mesh (*.stl *.ply)")
        self.static_label .setText(self.static_path.split("/")[-1])
        self.static = utility.read(self.static_path)
        self.parent.set_static_mesh(self.static)
        return

    @pyqtSlot()
    def choose_moving_mesh(self):
        self.moving_path, _ = QFileDialog.getOpenFileName(self, 'Open file', filter = "Mesh (*.stl *.ply)")
        self.moving_label.setText(self.moving_path.split("/")[-1])
        self.moving = utility.read(self.moving_path)
        self.parent.set_moving_mesh(self.moving)
        return

    def next_page(self):
        new_index = self.stacked_widget.currentIndex() + 1        
        self.change_btn()
        second_page = QWidget()
        self.stacked_widget.insertWidget(new_index, second_page)
        self.stacked_widget.setCurrentIndex(new_index)

        grid = QGridLayout()
        row = 0
        # List of checked checkboxes
        checked_cb = list(filter(lambda cb: cb.isChecked(), self.checkboxes.values()))
        priorities = list(range(len(checked_cb)))
        # Dictionary: registration name of checked checkboxes -> priority
        self.checked_cb_names = {}
        priorities = list(map(lambda x : str(x + 1), priorities))
        # Dictionary: registration name -> parameters
        self.methods_parameters = {}

        index = 0
        for reg, checkbox in self.checkboxes.items():
            
            if (checkbox.isChecked()):
                priority = QComboBox()
                priority.addItems(priorities)
                priority.setCurrentIndex(index)
                index += 1
                grid.addWidget(priority, row, 0)
                # Relate to registration name its priority combo box
                self.checked_cb_names[reg] = priority
               
                if (reg == self.landmarks_name):
                    label, run_button = self.lmk_reg_setting(grid, row)

                elif (reg == self.rigid_name):
                    label, run_button = self.vkt_icp_setting("RigidBody", grid, row)

                elif (reg == self.similarity_name):
                    label, run_button = self.vkt_icp_setting("Similarity", grid, row)

                elif (reg == self.affine_name):
                    label, run_button = self.vkt_icp_setting("Affine", grid, row)

                elif (reg == self.sanders_name):
                    label, run_button = self.sanders_setting(grid, row)

                elif (reg == self.tps_name):
                    label, run_button = self.tps_setting(grid, row)

                elif (reg == self.procrustes_name):
                    label, run_button = self.procrustes_setting(grid, row)

                grid.addWidget(label, row, 1)
                grid.addWidget(run_button, row, 2)
                row += 1
        second_page.setLayout(grid)

    def lmk_reg_setting(self, grid, row):
        label = QLabel("Landmarks registration")
        run_button = QPushButton("Set parameters")
        run_button.clicked.connect(self.get_lmk_parameters)
        return label, run_button

    def vkt_icp_setting(self, mode, grid, row):
        label = QLabel("ICP " + mode + " registration")
        run_button = QPushButton("Set parameters")
        default_parameters = ["RMS", mode, 200, 1, 0.00001, 600]
        if (mode == "RigidBody"):
            self.methods_parameters[self.rigid_name] = default_parameters
        elif (mode == "Similarity"):
            self.methods_parameters[self.similarity_name] = default_parameters
        else:
            self.methods_parameters[self.affine_name] = default_parameters
        run_button.clicked.connect(lambda: self.get_icp_parameters(mode))
        return label, run_button

    def sanders_setting(self, grid, row):
        label = QLabel("Sanders registration")
        run_button = QPushButton("Set parameters")
        self.methods_parameters[self.sanders_name] = [40, (1, 0), (0.8, 0.2)]
        run_button.clicked.connect(self.get_sanders_parameters)
        return label, run_button

    def tps_setting(self, grid, row):
        label = QLabel("Thin plate spline registration")
        run_button = QPushButton("Set parameters")
        run_button.clicked.connect(self.get_tps_parameters)
        return label, run_button

    def procrustes_setting(self, grid, row):
        label = QLabel("Procrustes registration")
        run_button = QPushButton("Set parameters")
        self.methods_parameters[self.procrustes_name] = ["RigidBody", []]
        run_button.clicked.connect(self.get_procrustes_parameters)
        return label, run_button

    def get_lmk_parameters(self):
        dialog = ParametersDialog("landmarks")
        self.methods_parameters[self.landmarks_name] = dialog.landmarks_parameters

    def get_icp_parameters(self, mode):
        dialog = ParametersDialog("icp", mode)
        if (mode == "RigidBody"):
            self.methods_parameters[self.rigid_name] = dialog.rigid_parameters
        elif (mode == "Similarity"):
            self.methods_parameters[self.similarity_name] = dialog.similarity_parameters
        else:
            self.methods_parameters[self.affine_name] = dialog.affine_parameters

    def get_sanders_parameters(self):
        dialog = ParametersDialog("sanders")
        self.methods_parameters[self.sanders_name] = dialog.sanders_parameters

    def get_tps_parameters(self):
        dialog = ParametersDialog("tps")
        self.methods_parameters[self.tps_name] = dialog.tps_parameters

    def get_procrustes_parameters(self):
        dialog = ParametersDialog("procrustes")
        self.methods_parameters[self.procrustes_name] = dialog.procrustes_parameters

    def run_registration(self):

        def f(x):
            return int(x.currentText())

        # Update prioroties with their current value in combo box
        self.final_priorities = {f(v): k for k, v in self.checked_cb_names.items()}
        # Order dictionary by key (priority)
        self.final_priorities = OrderedDict(sorted(self.final_priorities.items())) 
        self.actual_reg = 1
        self.output_matrices = []
        self.hbox.removeWidget(self.run_button)
        self.run_button = QPushButton()
        self.run_button.setText("Next registration")
        _, self.dir_path, self.file_name = file_handler.create_dir_by_filename(self.moving_path, "_reg")
        self.run_button.clicked.connect(lambda: self.run_single_registration_step(self.actual_reg))
        self.hbox.addWidget(self.run_button)
        self.run_single_registration_step(self.actual_reg)

    def run_single_registration_step(self, step) :

        save_name = os.path.join(self.dir_path, self.file_name + "_" + str(step))
        method = self.final_priorities[step]
        self.parent.add_log("Perform " + method)
        parameters = self.methods_parameters[method]

        if (method == self.landmarks_name):

            self.parent.add_log("Parameters: \n" + "Method: " + parameters[2])
            static_landmarks, moving_landmarks = file_handler.read_alignment_points(self.static, self.moving, parameters[0], parameters[1])
            transform = registration.run_landmarks_registration(self.static, self.moving, static_landmarks, moving_landmarks, parameters[2])
            transform.Inverse()
            transformMatrix = vtk.vtkMatrix4x4()
            transform.GetMatrix(transformMatrix)
            self.output_matrices.append(transformMatrix)
            self.parent.add_log("Output matrix: \n" + np.array_str(utility.vtkmatrix_to_numpy(transformMatrix)))
            self.moving = registration.apply_transformation(self.moving, transformMatrix)

        elif ((method == self.rigid_name) | (method == self.similarity_name) | (method == self.affine_name)):

            distance_type, reg_method, iterations, checkMeanDistance, maxDistance, numberOfLandmarks = parameters[0], parameters[1], parameters[2], parameters[3], parameters[4], parameters[5]
            self.parent.add_log("Parameters: \n" + "Distance type: " + distance_type + ", Method: " + reg_method + ", Iterations: " + str(iterations) + ", Check Mean Distance: " + str(checkMeanDistance) + ", Max distance: " + str(maxDistance) + ", Number of landmarks: " + str(numberOfLandmarks))
            icp = registration.run_icp_vtk(self.static, self.moving, distance_type, reg_method, iterations, checkMeanDistance, maxDistance, numberOfLandmarks)
            icp.Inverse() 
            transformMatrix = vtk.vtkMatrix4x4()
            icp.GetMatrix(transformMatrix)
            self.output_matrices.append(transformMatrix)
            self.parent.add_log("Output matrix: \n" + np.array_str(utility.vtkmatrix_to_numpy(transformMatrix)))
            self.moving = registration.apply_transformation(self.moving, transformMatrix)

        elif (method == self.sanders_name):

            self.parent.add_log("Parameters: \n" + "Iterations: " + str(parameters[0]) + ", First step weights: " + str(parameters[1]) + ", Second step weights: " + str(parameters[2]))
            static_amp_obj, moving_amp_obj = registration.load_ampscan_meshes(self.static_path, self.moving_path)
            alignment = registration.run_sanders_alignment(static_amp_obj, moving_amp_obj, parameters[0], [parameters[1], parameters[2]])
            matrix = alignment.tForm
            self.output_matrices.append(utility.npmatrix_to_vtk(matrix))
            self.parent.add_log("Output matrix: \n" + str(matrix))
            save_name = save_name + "_" + method + ".stl"
            alignment.m.save(save_name)
            self.moving = utility.read(save_name)

        elif (method == self.tps_name):

            self.parent.add_log("Parameters: \n" + "Sigma: " + str(parameters[2]))
            static_landmarks, moving_landmarks = file_handler.read_alignment_points(self.static, self.moving, parameters[0], parameters[1])
            self.moving = registration.run_thinPlateSpline_transform(self.moving, static_landmarks, moving_landmarks, parameters[2])

        elif (method == self.procrustes_name):

            self.parent.add_log("Parameters: \n" + "Method: " + parameters[0])
            meshes_paths = parameters[1]
            meshes = list(map(utility.read, meshes_paths))
            meshes.append(self.static)
            meshes.append(self.moving)
            procrustes = registration.run_procrustes_transform(meshes, parameters[0])
            res_meshes = [procrustes.GetOutput().GetBlock(i) for i in range(len(meshes))]
            self.parent.add_log("NB: Static mesh has " + str(self.static.GetNumberOfPoints()) + " and moving has " +
                                str(self.moving.GetNumberOfPoints()) + ". If they have different number of points or different topology algorithm will not work.")
            if (len(res_meshes) > 2) :
                for i, mesh in enumerate(res_meshes[2:]) :
                    registered_path = meshes_paths[i].split(".")[0] + "_" + method + ".ply"
                    utility.write(mesh, registered_path)
                    self.parent.add_mesh(registered_path)
            self.parent.set_static_mesh(res_meshes[0])
            self.moving = res_meshes[1]

        if (method != self.sanders_name):
            utility.write(self.moving, save_name + "_" + method + ".ply")

        self.parent.set_moving_mesh(self.moving)
        self.actual_reg += 1

        if (self.actual_reg not in self.final_priorities):
            self.close()
            transform = vtk.vtkTransform()
            transform.PostMultiply()
            for t in self.output_matrices :
                transform.Concatenate(t)
            transformMatrix = vtk.vtkMatrix4x4()
            transform.GetMatrix(transformMatrix)
            if (len(self.output_matrices) > 0) :
                self.parent.add_log("Final Matrix: \n" + np.array_str(utility.vtkmatrix_to_numpy(transformMatrix)))
            self.parent.add_other_mesh_application_window(transform)
