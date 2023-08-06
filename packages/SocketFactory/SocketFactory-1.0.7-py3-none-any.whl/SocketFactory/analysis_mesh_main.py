
from SocketFactory.gui_outcomes.gui_compare_mesh import CompareMeshVisGUI
from PyQt5.QtWidgets import *
import sys

def launch():
    app = QApplication(sys.argv)
    screen = app.primaryScreen()
    window = CompareMeshVisGUI(screen.size())
    sys.exit(app.exec_())

if __name__=='__main__':
    launch()
