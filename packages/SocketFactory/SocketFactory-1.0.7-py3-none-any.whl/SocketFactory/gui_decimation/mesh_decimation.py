from PyQt5.QtWidgets import *
from PyQt5.QtCore import pyqtSlot
import sys
import pymeshlab as ml

class decimationGUI(QMainWindow):
    """
    Basic interface that takes n meshes and applies decimation using a Quadric based Edge Collapse Strategy 
    (PyMeshlab Filter)
        Reduction percentage will be set by user input
    Output will be saved to original folder with 'dec' appended to the filename

    """ 
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Mesh percentage reduction')
        self.initGUI()

    def initGUI(self):

        self.width = 600
        self.height = 200
        self.resize(self.width, self.height)
        self.main_widget = QWidget()
        self.setCentralWidget(self.main_widget)
        grid = QGridLayout()
        grid.setSpacing(10)
        self.main_widget.setLayout(grid)
        grid.addWidget(self.files_selection(), 0, 0)
        
        self.show()

    @pyqtSlot()
    def files_selection(self):
        groupBox = QGroupBox("File selection")
        layout = QFormLayout()
        file_btn = QPushButton('Load mesh',self)
        file_btn.clicked.connect(self.choose_file)

        self.file_label = QLabel('', self)
        self.file_label.setWordWrap(True) 
        self.percentage = QSpinBox()
        self.percentage_label = QLabel("Percentage reduction")
        self.percentage.setRange(0, 100)
        self.percentage.setSingleStep(5)
        self.percentage.setSuffix(' %')
               
        run_btn = QPushButton('Apply decimation', self)
        run_btn.clicked.connect(self.run)
        run_btn.setStyleSheet("background-color : green")
        
        vbox = QVBoxLayout()
        vbox.addWidget(self.file_label)
        vbox.addWidget(file_btn)
        vbox.addWidget(self.percentage_label)
        vbox.addWidget(self.percentage)
        vbox.addWidget(run_btn)
        groupBox.setLayout(vbox)
        return groupBox

    @pyqtSlot()
    def choose_file(self):
        self.file_paths, _ = QFileDialog.getOpenFileNames(self, 'Open file', filter = "Meshes (*.stl *.ply)")
        final_label = ''
        for n in self.file_paths:
             final_label += n.split("/")[-1] + '\n'
        self.file_label.setText(final_label)
        return
    
    @pyqtSlot()
    def run (self):
        percentage = self.percentage.value()/100
        self.close()
        ms = ml.MeshSet()
        for p in self.file_paths:
            ms.load_new_mesh(p)
            ms.apply_filter('simplification_quadric_edge_collapse_decimation', targetperc = percentage)
            ms.save_current_mesh(p.split('.')[0] + '_dec.ply')
