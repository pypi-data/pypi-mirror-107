
from PyQt5.QtWidgets import *
from SocketFactory.gui_outcomes.outcome_visualization_window import OutcomeVisGui
import sys

def launch():
    app = QApplication(sys.argv)
    screen = app.primaryScreen()
    window = OutcomeVisGui(screen.size())
    sys.exit(app.exec_())
    
if __name__=='__main__':
    launch()

