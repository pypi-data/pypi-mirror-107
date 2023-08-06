
from SocketFactory.gui_pca.pca_main_window import PCAGui
from PyQt5.QtWidgets import *
import sys

def launch():
    app = QApplication(sys.argv)
    screen = app.primaryScreen()
    window = PCAGui(screen.size())
    window.setWindowTitle('Differential PCA')
    window.run_pca_btn.clicked.connect(lambda: window.run_pca(True))
    sys.exit(app.exec_())
    
if __name__=='__main__':
    launch()


