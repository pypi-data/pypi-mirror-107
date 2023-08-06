
from SocketFactory.gui_decimation.mesh_decimation import decimationGUI
from PyQt5.QtWidgets import *
import sys

def launch():
    app = QApplication(sys.argv)
    window = decimationGUI()
    sys.exit(app.exec_())
    
if __name__=='__main__':
    launch()


