
from PyQt5.QtWidgets import *
import sys
from SocketFactory.gui_registration.mesh_visualization_window import MeshRegistrationGui

def launch():
    app = QApplication(sys.argv)
    screen = app.primaryScreen()
    window = MeshRegistrationGui(screen.size())
    sys.exit(app.exec_())
    
if __name__=='__main__':
    launch()
