
from PyQt5.QtWidgets import *
import sys
from SocketFactory.gui_outcomes.gui_slices import SlicerGui                                                           

def launch():
    app = QApplication(sys.argv)
    window = SlicerGui()
    sys.exit(app.exec_())
      
if __name__=='__main__':
    launch()                                                           
                        