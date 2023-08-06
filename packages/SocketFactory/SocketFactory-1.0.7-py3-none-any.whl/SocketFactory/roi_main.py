
from PyQt5.QtWidgets import *
import sys
from SocketFactory.gui_outcomes.gui_roi_selection import ROIGui

def launch():
    app = QApplication(sys.argv)
    screen = app.primaryScreen()
    window = ROIGui(screen.size())
    sys.exit(app.exec_())  
      
if __name__=='__main__':
    launch()                                                           
                                                                                                                                     