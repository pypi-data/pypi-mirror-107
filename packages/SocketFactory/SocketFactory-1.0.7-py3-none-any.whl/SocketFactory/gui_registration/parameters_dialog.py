
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

class ParametersDialog(QDialog):

     def __init__(self, registration, mode = ""):
        super().__init__()
        self.setWindowTitle('Set Parameters')
        self.resize(400, 200)
        self.buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.buttonBox.rejected.connect(self.reject)
        if (registration == "landmarks"):
            self.init_lmk_reg()
        elif (registration == "icp"):
            self.init_icp(mode)
        elif (registration == "sanders"):
            self.init_sanders()
        elif (registration == "tps"):
            self.init_tps()
        elif (registration == "procrustes"):
            self.init_procrustes()
        mainLayout = QVBoxLayout()
        self.setLayout(mainLayout)
        mainLayout.addWidget(self.formGroupBox)
        mainLayout.addWidget(self.buttonBox)
        self.exec_()

     def init_lmk_reg(self): 
        self.formGroupBox = QGroupBox("Set landmarks registration parameters")
        layout = QFormLayout()

        self.lmk_reg_method = QComboBox()
        self.lmk_reg_method.addItems(["RigidBody", "Similarity", "Affine"])
        layout.addRow(QLabel("Registration mode:"), self.lmk_reg_method)

        grid = QGridLayout()
        static_lmk_btn = QPushButton("Select static landmarks")
        static_lmk_btn.clicked.connect(self.select_static_lmk)
        self.static_lmk_label = QLabel()
        grid.addWidget(static_lmk_btn, 0, 0)
        grid.addWidget(self.static_lmk_label, 0, 1)

        moving_lmk_btn = QPushButton("Select moving landmarks")
        moving_lmk_btn.clicked.connect(self.select_moving_lmk)
        self.moving_lmk_label = QLabel()
        grid.addWidget(moving_lmk_btn, 1, 0)
        grid.addWidget(self.moving_lmk_label, 1, 1)
        layout.addRow(grid)
        self.formGroupBox.setLayout(layout)
        self.buttonBox.accepted.connect(self.accept_lmk_parameters)

     def select_static_lmk(self):
        self.static_lmk_path, _ = QFileDialog.getOpenFileName(self, 'Open file', filter = "Text *.txt")
        self.static_lmk_label .setText(self.static_lmk_path.split("/")[-1])

     def select_moving_lmk(self):
        self.moving_lmk_path, _ = QFileDialog.getOpenFileName(self, 'Open file', filter = "Text *.txt")
        self.moving_lmk_label .setText(self.moving_lmk_path.split("/")[-1])

     def accept_lmk_parameters(self):
        self.landmarks_parameters = [self.static_lmk_path, self.moving_lmk_path, self.lmk_reg_method.currentText()]
        self.done(0)

     def init_icp(self, mode):
        self.formGroupBox = QGroupBox("Set icp parameters")
        layout = QFormLayout()

        self.mean_dist_combo = QComboBox()
        self.mean_dist_combo.addItems(["RMS", "Absolute Value"])
        layout.addRow(QLabel("Mean Distance Type:"), self.mean_dist_combo)

        self.checkMeanDistance_combo = QComboBox()
        self.checkMeanDistance_combo.addItems(["Yes", "No"])
        layout.addRow(QLabel("Check mean distance:"), self.checkMeanDistance_combo)

        self.maxDistance_spin_box = QDoubleSpinBox()
        self.maxDistance_spin_box.setDecimals(7)
        self.maxDistance_spin_box.setValue(0.00001)
        layout.addRow(QLabel("Max Distance:"), self.maxDistance_spin_box)

        self.iterations_spin_box = QSpinBox()
        self.iterations_spin_box.setMaximum(1000)
        self.iterations_spin_box.setValue(200)
        layout.addRow(QLabel("Iterations:"), self.iterations_spin_box)

        self.lmk_spin_box = QSpinBox()
        self.lmk_spin_box.setMaximum(1000)
        self.lmk_spin_box.setValue(600)
        layout.addRow(QLabel("Number of landmarks:"), self.lmk_spin_box)

        self.buttonBox.accepted.connect(lambda: self.accept_icp_parameters(mode))
        self.formGroupBox.setLayout(layout)

     def accept_icp_parameters(self, mode):
        checkMeanDist = True if (self.checkMeanDistance_combo.currentText() == "Yes") else False
        parameters = [self.mean_dist_combo.currentText(), mode, self.iterations_spin_box.value(), checkMeanDist, self.maxDistance_spin_box.value(), self.lmk_spin_box.value()]
        if (mode == "RigidBody") :
            self.rigid_parameters = parameters
        elif (mode == "Similarity") :
            self.similarity_parameters = parameters
        else :
            self.affine_parameters = parameters
        self.done(0)

     def init_sanders(self):

        self.formGroupBox = QGroupBox("Set Sanders parameters")
        layout = QFormLayout()

        self.iterations_spin_box = QSpinBox()
        self.iterations_spin_box.setMaximum(1000)
        self.iterations_spin_box.setValue(40)
        self.re_1_weight_spin_box = QDoubleSpinBox()
        self.re_1_weight_spin_box.setValue(1)
        self.sim_1_weight_spin_box = QDoubleSpinBox()
        self.sim_1_weight_spin_box.setValue(0)
        self.re_2_weight_spin_box = QDoubleSpinBox()
        self.re_2_weight_spin_box.setValue(0.8)
        self.sim_2_weight_spin_box = QDoubleSpinBox()
        self.sim_2_weight_spin_box.setValue(0.2)
        layout.addRow(QLabel("Iterations:"), self.iterations_spin_box)
        layout.addRow(QLabel("First step re weight:"), self.re_1_weight_spin_box)
        layout.addRow(QLabel("First step similarity weight:"), self.sim_1_weight_spin_box)
        layout.addRow(QLabel("Second step re weight:"), self.re_2_weight_spin_box)
        layout.addRow(QLabel("Second step similarity weight:"), self.sim_2_weight_spin_box)
        self.formGroupBox.setLayout(layout)

        self.buttonBox.accepted.connect(self.accept_sanders_parameters)
      
     def accept_sanders_parameters(self):
        self.sanders_parameters = [self.iterations_spin_box.value(), (self.re_1_weight_spin_box.value(), self.sim_1_weight_spin_box.value()), (self.re_2_weight_spin_box.value(), self.sim_2_weight_spin_box.value())]
        self.done(0)

     def init_tps(self):
        self.formGroupBox = QGroupBox("Set Thin plate spline parameters")
        layout = QFormLayout()

        self.sigma_spin_box = QDoubleSpinBox()
        self.sigma_spin_box.setValue(1)
        layout.addRow(QLabel("Sigma:"), self.sigma_spin_box)

        grid = QGridLayout()
        static_lmk_btn = QPushButton("Select static landmarks")
        static_lmk_btn.clicked.connect(self.select_static_lmk)
        self.static_lmk_label = QLabel()
        grid.addWidget(static_lmk_btn, 0, 0)
        grid.addWidget(self.static_lmk_label, 0, 1)

        moving_lmk_btn = QPushButton("Select moving landmarks")
        moving_lmk_btn.clicked.connect(self.select_moving_lmk)
        self.moving_lmk_label = QLabel()
        grid.addWidget(moving_lmk_btn, 1, 0)
        grid.addWidget(self.moving_lmk_label, 1, 1)
        layout.addRow(grid)
        self.formGroupBox.setLayout(layout)

        self.buttonBox.accepted.connect(self.accept_tps_parameters)

     def accept_tps_parameters(self):
        self.tps_parameters = [self.static_lmk_path, self.moving_lmk_path, self.sigma_spin_box.value()]
        self.done(0)

     def init_procrustes(self):
        self.formGroupBox = QGroupBox("Set Procrustes parameters")
        layout = QFormLayout()
        self.proc_reg_method = QComboBox()
        self.proc_reg_method.addItems(["RigidBody", "Similarity", "Affine"])
        layout.addRow(QLabel("Registration mode:"), self.proc_reg_method)

        grid = QGridLayout()
        self.procrustes_meshes_paths = []
        procrustes_meshes_btn = QPushButton("Select other meshes")
        procrustes_meshes_btn.clicked.connect(self.select_procrustes_meshes)
        self.procrustes_meshes_label = QLabel()
        grid.addWidget(procrustes_meshes_btn, 0, 0)
        grid.addWidget(self.procrustes_meshes_label, 0, 1)
        layout.addRow(grid)
        self.formGroupBox.setLayout(layout)

        self.buttonBox.accepted.connect(self.accept_procrustes_parameters)

     def select_procrustes_meshes(self):
        self.procrustes_meshes_paths, _ = QFileDialog.getOpenFileNames(self, 'Open file', filter = "Meshes (*.stl *.ply)")
        final_label = ''
        for n in self.procrustes_meshes_paths:
             final_label += n.split("/")[-1] + '\n'
        self.procrustes_meshes_label.setText(final_label)
    
     def accept_procrustes_parameters(self):
        self.procrustes_parameters = [self.proc_reg_method.currentText(), self.procrustes_meshes_paths]
        self.close()
        
     def reject(self):
        self.done(0)