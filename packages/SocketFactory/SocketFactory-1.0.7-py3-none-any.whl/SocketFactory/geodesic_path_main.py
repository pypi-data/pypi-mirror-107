
from SocketFactory.gui_outcomes.gui_geodesic_distance import GeodesicGui
from PyQt5.QtWidgets import *
import sys

def launch():
    app = QApplication(sys.argv)
    window = GeodesicGui()
    sys.exit(app.exec_())
    
if __name__=='__main__':
    launch()



