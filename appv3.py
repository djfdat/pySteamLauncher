import os
import sys

from subprocess import Popen

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

import vdf


class Game(object):
    def __init__(self, gameData):
        self.name = gameData["name"]
        self.appid = gameData["appid"]

def GetSelectedGameID():
    return Games[list.selectedIndexes()[0].model().item(list.selectedIndexes()[0].row()).text()]

def OnDoubleClick():
    gameId = GetSelectedGameID()
    print("Launching game: " + str(gameId))
    Popen([steamPath, "steam://run/" + str(gameId)])

def SetSelectedGame(selected, deselected):
    print("working")
    print(str(list.selectedIndexes))

def getMaxLibraryFolder(data, checkIndex=0):
    try:
        if data[str(checkIndex + 1)]:
            return getMaxLibraryFolder(data, checkIndex + 1)
    except KeyError:
            return checkIndex

    return checkIndex





# Create a Qt application
app = QApplication(sys.argv)

steamRootPath = "C:\\Program Files (x86)\\Steam"
steamPath = steamRootPath + "\\steam.exe"
librariesPath = steamRootPath + "\\steamapps\\libraryfolders.vdf"


Games = {}
gamesList = []


librariesData = vdf.load(open(librariesPath))
libraryPaths = []
libraryPaths.append(steamRootPath + "\\steamapps\\")
libraryPaths.append(librariesData["LibraryFolders"]["1"] + "\\\\steamapps\\\\")
numPaths = getMaxLibraryFolder(librariesData["LibraryFolders"])

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

# Our main window will be a QListView
list = QListView()
list.setWindowTitle('pySteamLauncher')
list.setMinimumSize(800, 600)
# list.setWindowIcon(QtGui.QIcon('logo.png'))

list.doubleClicked.connect(OnDoubleClick) # Launch Game


# Create an empty model for the list's data
model = QStandardItemModel(list)

for gameName, gameId in Games.items():
    game = QStandardItem(gameName)
    game.setEditable(False)
    model.appendRow(game)

# Apply the model to the list view
list.setModel(model)
# Select first option by default
list.setCurrentIndex(list.model().index(0,0)) # Show the window and run the app
list.show()
app.exec_()