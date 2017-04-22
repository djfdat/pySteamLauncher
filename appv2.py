import sys
from PyQt5 import (QtGui, QtWidgets, QtCore)
import qdarkstyle

class MainWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()
        self.resize(800, 600)
        self.setWindowTitle("pySteamLauncher")
        self.setWindowIcon(QtGui.QIcon('logo.png'))

        # extractAction = QtWidgets.QAction("Exit", self)
        # extractAction.setShortcut("Escape")
        # extractAction.setStatusTip("Exit")
        # extractAction.triggered.connect(self.closeApplication)

        # self.statusBar()

        # mainMenu = self.menuBar()
        # fileMenu = mainMenu.addMenu('&File')
        # fileMenu.addAction(extractAction)

        # self.home()

        # self.searchField()
        self.resultsList()
        self.show()

    def searchField(self):
        txtSearchField = QtWidgets.QLineEdit(self)
        txtSearchField.move(0, 0)
        txtSearchField.textChanged.connect(self.on_searchField_textChanged)

    def resultsList(self):
        scrollArea = QtWidgets.QScrollArea(self)



    def home(self):
        # btn = QtWidgets.QPushButton("Exit", self)
        # btn.move(0, 100)
        # btn.clicked.connect(self.closeApplication)
        pass

    def closeApplication(self):
        sys.exit()

    def on_searchField_textChanged(self):
        pass

def run():
    app = QtWidgets.QApplication(sys.argv)
    # app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    mainWindow = MainWindow()
    sys.exit(app.exec_())

run()