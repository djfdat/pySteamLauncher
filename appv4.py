import os
import sys

from subprocess import Popen

from Qt.QtCore import QEvent
from Qt.QtWidgets import QWidget, QLineEdit, QGridLayout, QApplication, QListView
from Qt.QtGui import QIcon, QStandardItemModel, QStandardItem

import vdf

class Game(object):
    def __init__(self, gameData):
        self.name = gameData["name"]
        self.appid = gameData["appid"]

class pySteamLauncherWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.BuildGamesList()
        self.initUI()

    def BuildGamesList(self):
        self.steamRootPath = "C:\\Program Files (x86)\\Steam"
        self.steamPath = self.steamRootPath + "\\steam.exe"
        librariesPath = self.steamRootPath + "\\steamapps\\libraryfolders.vdf"

        self.Games = {}
        self.gamesList = []


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
                    self.gamesList.append(Game(gameData))

        for game in self.gamesList:
            self.Games[game.name] = game.appid

    def GetSelectedGame(self):
        return self.list.selectedIndexes()[0].model().item(self.list.selectedIndexes()[0].row()).text()

    def GetSelectedGameID(self):
        return self.Games[self.GetSelectedGame()]

    def OnDoubleClick(self):
        gameId = self.GetSelectedGameID()
        print("Launching Game: " + str(gameId))
        Popen([self.steamPath, "steam://run/" + str(gameId)])
        sys.exit(app.exec_())

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

        self.list = QListView()
        # Create an empty model for the list's data
        model = QStandardItemModel(self.list)

        for gameName, gameId in self.Games.items():
            game = QStandardItem(gameName)
            game.setEditable(False)
            model.appendRow(game)

        self.list.doubleClicked.connect(self.OnDoubleClick) # Launch Game
        # Apply the model to the list view
        self.list.setModel(model)
        self.list.setCurrentIndex(self.list.model().index(0, 0)) # Show the window and run the app

        grid.addWidget(self.list, 2, 0)

        self.setLayout(grid)

        self.setGeometry(300, 300, 350, 300)
        self.setWindowTitle('pySteamLauncher')
        self.setWindowIcon(QIcon('logo.png'))
        self.show()

class pySteamLauncher(QApplication):
    def __init__(self, args):
        super(pySteamLauncher, self).__init__(args)
        self.window = pySteamLauncherWindow()

    def notify(self, receiver, event):
        if event.type() == QEvent.KeyPress:
            print(type(receiver))
            if type(receiver) != "<class 'PyQt5.QtGui.QWindow'>":
                pass
            elif event.key() == 16777216: # Escape
                self.quit()
            elif event.key() == 16777220 or event.key() == 16777221: #Return and Enter
                self.window.OnDoubleClick()
                self.quit()
            elif event.key() == 16777235: # Up
                pass
            elif event.key() == 16777237: # Down
                pass

        #Call Base Class Method to Continue Normal Event Processing
        return super(pySteamLauncher, self).notify(receiver, event)


if __name__ == '__main__':
    app = pySteamLauncher(sys.argv)
    sys.exit(app.exec_())