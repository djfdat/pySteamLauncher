import os
import sys
from subprocess import Popen

# PyQT5 Widgets and accessories
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

# from PyQt5.QtWidgets import (
#     QApplication,
#     QWidget,
#     QToolTip,
#     QLineEdit,
#     QPushButton,
#     QHBoxLayout,
#     QVBoxLayout,
#     QDesktopWidget,
#     QScrollArea
# )
# from PyQt5.QtGui import QFont
import qdarkstyle

# Library for handling config.vdf
import vdf

class Game(object):
    def __init__(self, gameData):
        self.name = gameData["name"]
        self.appid = gameData["appid"]

class Application(QWidget):

    gamesList = []

    def __init__(self):
        super().__init__()
        self.initUI()

    def make_OnClick_LaunchGame(self, gameId):
        def OnClick_LaunchGame():
            print("Launching game: " + gameId)
            Popen([self.steamPath, "steam://run/" + gameId])

        return OnClick_LaunchGame

    def getMaxLibraryFolder(self, data, checkIndex=0):
        try:
            if data[str(checkIndex + 1)]:
                return self.getMaxLibraryFolder(data, checkIndex + 1)
        except KeyError:
                return checkIndex

        return checkIndex


    def OnClick_LoadConfig(self):
        print("Loading Configuration")

        # rootPath = self.txtLoadConfigurationPath.text()
        rootPath = "C:\\Program Files (x86)\\Steam"

        if rootPath == "":
            print("No root path set. Defaulting to 'C:\\Program Files (x86)\\Steam'")
            self.steamRootPath = "C:\\Program Files (x86)\\Steam"
        else:
            self.steamRootPath = rootPath

        self.steamPath = self.steamRootPath + "\\steam.exe"
        self.librariesPath = self.steamRootPath + "\\steamapps\\libraryfolders.vdf"

        librariesData = vdf.load(open(self.librariesPath))

        libraryPaths = []
        libraryPaths.append(self.steamRootPath + "\\steamapps\\")

        libraryPaths.append(librariesData["LibraryFolders"]["1"] + "\\\\steamapps\\\\")
        numPaths = self.getMaxLibraryFolder(librariesData["LibraryFolders"])

        if numPaths > 0:
            for i in range(1, numPaths):
                libraryPaths.append(librariesData["LibraryFolders"][str(i)] + "\\\\steamapps\\\\")

        for libraryPath in libraryPaths:
            for file in os.listdir(libraryPath):
                if file.endswith(".acf"):
                    gameData = vdf.load(open(libraryPath + file))
                    gameData = gameData["AppState"]
                    self.gamesList.append(Game(gameData))

        for game in self.gamesList:
            btnGameButton = QPushButton(game.name, self)
            btnGameButton.clicked.connect(self.make_OnClick_LaunchGame(game.appid))
            self.vboxGamesListContainer.addWidget(btnGameButton)

    def generateLoadConfigurationView(self):
        QToolTip.setFont(QFont('SansSerif', 10))

        btnLoadConfig = QPushButton('Load Config', self)
        btnLoadConfig.setToolTip('Load Configuration File.')
        btnLoadConfig.resize(btnLoadConfig.sizeHint())
        btnLoadConfig.clicked.connect(self.OnClick_LoadConfig)

        self.txtLoadConfigurationPath = QLineEdit(self)
        self.txtLoadConfigurationPath.setPlaceholderText("C:\\Program Files (x86)\\Steam")
        self.txtLoadConfigurationPath.resize(280, 40)

        hbox = QHBoxLayout()
        hbox.addWidget(self.txtLoadConfigurationPath)
        hbox.addWidget(btnLoadConfig)
        return hbox

    def generateGameListView(self):
        self.vboxGamesListScrollArea = QScrollArea(self)
        self.vboxWidgetContainer = QWidget(self)
        self.vboxGamesListContainer = QVBoxLayout()

        self.vboxWidgetContainer.setLayout(self.vboxGamesListContainer)
        self.vboxGamesListScrollArea.setWidget(self.vboxWidgetContainer)

        self.vboxWidgetContainer.setMinimumWidth(600)
        self.vboxWidgetContainer.move(80, 160)
        # self.vboxGamesListContainer.move(80, 100)

        return self.vboxWidgetContainer

    def generateSearchField(self):
        self.txtSearchField = QLineEdit(self)
        self.txtSearchField.textChanged.connect(self.OnSearchTextUpdated)

        return self.txtSearchField

    def generateMainLayout(self):
        pass

    def OnSearchTextUpdated(self):
        pass

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def initUI(self):
        # vbox.addLayout(self.generateLoadConfigurationView())
        vbox = QVBoxLayout()
        vbox.addWidget(self.generateSearchField())
        vbox.addWidget(self.generateGameListView())

        self.setLayout(vbox)

        self.resize(800, 600)
        self.setMinimumSize(800, 600)
        self.center()
        self.setWindowTitle('pySteamLauncher')
        self.setWindowIcon(QIcon('logo.png'))
        self.show()

        # Placeholder to auto-initialize
        self.OnClick_LoadConfig()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    ex = Application()
    sys.exit(app.exec_())
