import re
import sys

import dxfgrabber
from PyQt4 import Qt


import forlinelist      # Для заполнения выпадающего списка названиями районов
from forfind import findrastres  # Функция поиска по координатам

class MainWindow(Qt.QMainWindow):
    def __init__(self, parent=None):
        Qt.QMainWindow.__init__(self,parent)
        self.setWindowTitle('Find rastres')
        widgets = Qt.QWidget()
        self.setCentralWidget(widgets)
        icon_app = Qt.QIcon("eye.png")
        icon_exit = Qt.QIcon("power.png")
        self.setWindowIcon(icon_app)
        exit_menu = Qt.QAction(icon_exit, "Exit", self)
        exit_menu.setShortcut('Ctrl+Q')
        exit_menu.setStatusTip('Exit application')
        self.connect(exit_menu, Qt.SIGNAL("triggered()"), Qt.SLOT('close()'))
        msg1 = Qt.QMessageBox(widgets)
        msg1.setWindowTitle("Exit")
        menu = self.menuBar()
        file = menu.addMenu('&File')
        file.addAction(exit_menu)

app = Qt.QApplication(sys.argv)
mainwindow = MainWindow()
mainwindow.show()
sys.exit(app.exec_())