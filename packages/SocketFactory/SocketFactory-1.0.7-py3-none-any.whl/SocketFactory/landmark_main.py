
from SocketFactory.gui_landmark.landmark_selection import LandMarkSelectionModeGui
from PyQt5.QtWidgets import *
import sys

def launch():
    app = QApplication(sys.argv)
    screen = app.primaryScreen()
    window = LandMarkSelectionModeGui(screen.size())
    sys.exit(app.exec_())
    
if __name__=='__main__':
    launch()
