
from SocketFactory.gui_alignment.alignment_visualization_window import AlignmentVisGui
from PyQt5.QtWidgets import *
import sys

def launch():
    app = QApplication(sys.argv)
    screen = app.primaryScreen()
    window = AlignmentVisGui(screen.size())
    sys.exit(app.exec_())

if __name__=='__main__':
    launch()