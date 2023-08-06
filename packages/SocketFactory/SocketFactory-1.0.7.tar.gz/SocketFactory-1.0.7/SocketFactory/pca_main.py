
from PyQt5.QtWidgets import *
import sys
from SocketFactory.gui_pca.pca_main_window import PCAGui

def launch():
    app = QApplication(sys.argv)
    screen = app.primaryScreen()
    window = PCAGui(screen.size())
    window.setWindowTitle('PCA')
    window.run_pca_btn.clicked.connect(window.run_pca)
    sys.exit(app.exec_())
    
if __name__=='__main__':
    launch()

