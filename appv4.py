import os
import sys

from subprocess import Popen

from PyQt5.QtWidgets import (QWidget, QLabel, QLineEdit,
    QTextEdit, QGridLayout, QApplication, QListView)
from PyQt5.QtGui import (QIcon, QStandardItemModel, QStandardItem)

import vdf

class Game(object):
    def __init__(self, gameData):
        self.name = gameData["name"]
        self.appid = gameData["appid"]

class pySteamLauncher(QWidget):

    def __init__(self):
        super().__init__()

        self.initUI()

    def GetSelectedGameID(self):
        return Games[self.list.selectedIndexes()[0].model().item(self.list.selectedIndexes()[0].row()).text()]

    def OnDoubleClick(self):
        gameId = self.GetSelectedGameID()
        print("Launching game: " + str(gameId))
        Popen([self.steamPath, "steam://run/" + str(gameId)])

    def SetSelectedGame(self, selected, deselected):
        print("working")
        print(str(self.list.selectedIndexes))

    def getMaxLibraryFolder(self, data, checkIndex=0):
        try:
            if data[str(checkIndex + 1)]:
                return self.getMaxLibraryFolder(data, checkIndex + 1)
        except KeyError:
                return checkIndex

        return checkIndex

    def initUI(self):

        searchEdit = QLineEdit()
        grid = QGridLayout()
        grid.setSpacing(10)

        grid.addWidget(searchEdit, 1, 0)

        self.steamRootPath = "C:\\Program Files (x86)\\Steam"
        self.steamPath = self.steamRootPath + "\\steam.exe"
        librariesPath = self.steamRootPath + "\\steamapps\\libraryfolders.vdf"


        Games = {}
        gamesList = []


        librariesData = vdf.load(open(librariesPath))
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
                    gamesList.append(Game(gameData))

        for game in gamesList:
            Games[game.name] = game.appid

        self.list = QListView()
        # Create an empty model for the list's data
        model = QStandardItemModel(self.list)

        for gameName, gameId in Games.items():
            game = QStandardItem(gameName)
            game.setEditable(False)
            model.appendRow(game)

        self.list.doubleClicked.connect(self.OnDoubleClick) # Launch Game
        # Apply the model to the list view
        self.list.setModel(model)
        self.list.setCurrentIndex(self.list.model().index(0,0)) # Show the window and run the app

        grid.addWidget(self.list, 2, 0)

        self.setLayout(grid)

        self.setGeometry(300, 300, 350, 300)
        self.setWindowTitle('pySteamLauncher')
        self.setWindowIcon(QIcon('logo.png'))
        self.show()


if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = pySteamLauncher()
    sys.exit(app.exec_())