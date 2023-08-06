from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import os.path
import numpy as np
import pyvista as pv
from SocketFactory.utilities import utility, file_handler

class PCAHandlingWindow(QWidget):

    def __init__(self, parent, differential = False):
        super().__init__()
        self.parent = parent
        self.initGUI()
        self.differential = differential
        self.insert_first_page()

    def initGUI(self):
        
        self.stacked_widget = QStackedWidget()
        self.hbox = QHBoxLayout()
        vbox = QVBoxLayout()
        vbox.addWidget(self.stacked_widget)
        vbox.addLayout(self.hbox)
        self.setLayout(vbox)

    def insert_first_page(self, index=-1):
        first_page = QWidget()
        layout = QGridLayout()
        components_selection_label = QLabel("Select components indices to keep")
        components_selection_label.setFont(QFont("Arial", 12))
        starting_index_label =  QLabel("Starting index")
        self.starting_index_spinbox = QSpinBox()
        self.starting_index_spinbox.valueChanged.connect(self.update_explained_variance)
        self.starting_index_spinbox.setMaximum(self.parent.pca.f - 1)

        ending_index_label =  QLabel("Ending index")
        self.ending_index_spinbox = QSpinBox()
        self.ending_index_spinbox.setValue(self.parent.pca.f - 1)
        self.ending_index_spinbox.valueChanged.connect(self.update_explained_variance)
        self.ending_index_spinbox.setMaximum(self.parent.pca.f - 1)
        self.explained_variance_label = QLabel("")
        self.explained_variance_label.setFont(QFont("Arial", 12))
        next_btn = QPushButton("Next")
        next_btn.clicked.connect(self.next_page)

        layout.addWidget(components_selection_label, 0, 0, 1, 4)
        layout.addWidget(starting_index_label, 1, 0)
        layout.addWidget(self.starting_index_spinbox, 1, 1)
        layout.addWidget(ending_index_label, 1, 2)
        layout.addWidget(self.ending_index_spinbox, 1, 3)
        layout.addWidget(self.explained_variance_label, 2, 0, 1, 4)
        layout.addWidget(next_btn, 3, 0, 1, 4)

        first_page.setLayout(layout)
        self.update_explained_variance()
        vbox = QVBoxLayout()
        vbox.addStretch(1)
       
        self.stacked_widget.insertWidget(index, first_page)

    def update_explained_variance(self):
        text = "Explained variance is "
        explained_variance = self.parent.pca.lamda_ratios
        self.starting_index = self.starting_index_spinbox.value()
        self.ending_index = self.ending_index_spinbox.value()
        actual_explained_variance = round(sum(explained_variance[self.starting_index : (self.ending_index + 1)]), 4)
        self.explained_variance_label.setText(text + str(actual_explained_variance))

    def next_page(self):

        self.parent.pca.select_components(self.starting_index, self.ending_index + 1)
        new_index = self.stacked_widget.currentIndex() + 1 

        second_page = QWidget()
        scroll = QScrollArea()
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        scroll.setWidgetResizable(True)
        scroll.setWidget(second_page)

        self.stacked_widget.insertWidget(new_index, scroll)
        self.stacked_widget.setCurrentIndex(new_index)
        layout = QGridLayout()
        self.weights_spin_box = [QDoubleSpinBox() for i in range(self.ending_index - self.starting_index + 1)]
        [spinbox.setMinimum(-3) for spinbox in self.weights_spin_box]
        [spinbox.setMaximum(3) for spinbox in self.weights_spin_box]

        save_parameters_btn = QPushButton("Save PCA parameters")
        save_parameters_btn.clicked.connect(self.save_pca_parameters)

        form_layout = QFormLayout()
        for i, s in enumerate(self.weights_spin_box):
            form_layout.addRow(QLabel(str(i + self.starting_index) + " component"), s)

        layout.addWidget(save_parameters_btn, 0, 0, 1, 4)
        layout.addLayout(form_layout, 1, 0, 1, 4)
        if (not self.differential):
            
            generate_shape_btn = QPushButton("Generate shape")
            generate_shape_btn.clicked.connect(self.generate_shape)
            self.file_name_line_edit = QLineEdit("Insert file name")
            save_shape_btn = QPushButton("Save shape")
            save_shape_btn.clicked.connect(self.save_shape)
            layout.addWidget(generate_shape_btn, 2, 0, 1, 4)
            layout.addWidget(self.file_name_line_edit, 3, 0, 1, 2)
            layout.addWidget(save_shape_btn, 3, 2, 1, 2)

        else: 
            self.select_base_mesh_label = QLabel("")
            select_base_mesh_btn = QPushButton("Select base mesh")
            select_base_mesh_btn.clicked.connect(self.select_base_mesh)
            generate_shape_btn = QPushButton("Generate shape")
            generate_shape_btn.clicked.connect(self.generate_differential_shape)
            self.file_name_line_edit = QLineEdit("Insert file name")
            save_shape_btn = QPushButton("Save shape")
            save_shape_btn.clicked.connect(self.save_shape)
            layout.addWidget(self.select_base_mesh_label, 2, 0, 1, 2)
            layout.addWidget(select_base_mesh_btn, 2, 2, 1, 2)
            layout.addWidget(generate_shape_btn, 3, 0, 1, 4)
            layout.addWidget(self.file_name_line_edit, 4, 0, 1, 2)
            layout.addWidget(save_shape_btn, 4, 2, 1, 2)

        second_page.setLayout(layout)

    def save_pca_parameters(self):

        file_name = "pca_parameters.xlsx" if not self.differential else "diff_pca_parameters.xlsx"
        file_handler.create_pca_output_file(self.parent.pca, os.path.join(self.parent.dir_path, file_name))

    def generate_shape(self):
        """
        Generate shape through PCA.
        """

        self.weights = list(map(lambda s : s.value(), self.weights_spin_box))
        self.generated_shape = self.parent.pca.generate_shape(self.weights)
        self.parent.show_mesh(self.generated_shape)

    def save_shape(self):
        """
        Saving of generated shape.
        """

        file_name = os.path.join(self.parent.dir_path, self.file_name_line_edit.text())
        utility.write(self.generated_shape, file_name + ".stl")
        file = open(file_name + ".txt", "w+")
        for index, weight in zip(np.arange(self.starting_index, self.ending_index + 1, 1), self.weights):
            file.write("Component " + str(index) +": "+ str(weight) + "\n")
        file.close()
        self.file_name_line_edit.setText("Insert file name")

    @pyqtSlot()
    def select_base_mesh(self):
        self.mesh_path, _ = QFileDialog.getOpenFileName(self, 'Open file', filter = "Meshes (*.stl *.ply)")
        self.select_base_mesh_label.setText(self.mesh_path.split('/')[-1])
        return

    def generate_differential_shape(self):
        """
        Shape generation using differential PCA
        """

        self.weights = list(map(lambda s : s.value(), self.weights_spin_box))
        self.generated_shape = self.parent.pca.get_shape_from_differential_pca(self.weights, pv.read(self.mesh_path))
        self.parent.show_mesh(self.generated_shape)
