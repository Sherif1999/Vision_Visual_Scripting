from qtpy.QtGui import *
from qtpy.QtWidgets import *
from qtpy.QtCore import *

from nodeeditor.node_scene_history import SceneHistory


class settingsWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.masterRef = None

        self.settingsList = [[Appearance.__name__,Appearance], [KeyMapping.__name__,KeyMapping]]

        self.settingsLayout = QVBoxLayout()
        self.setLayout(self.settingsLayout)

        self.settingsSplitter = QSplitter(Qt.Horizontal)
        self.settingsLayout.addWidget(self.settingsSplitter)
        self.settingsSplitter.setChildrenCollapsible(False)

        # 1
        self.settingsTree = QTreeWidget()
        self.settingsTree.header().hide()
        self.settingsTree.setMaximumWidth(250)
        self.settingsTree.setMinimumWidth(150)
        self.settingsSplitter.addWidget(self.settingsTree)

        # 1
        for Item in self.settingsList:
            self.Setting = QTreeWidgetItem([Item[0]])
            self.Setting.setData(5, 6, Item[1])
            self.settingsTree.addTopLevelItem(self.Setting)

        # 2
        self.settingsWidget = QWidget()
        self.settingsSplitter.addWidget(self.settingsWidget)

        self.settingsTree.clicked.connect(self.settingsWidgetChange)

    def settingsWidgetChange(self):
        selected = self.settingsTree.selectedItems()
        old = self.settingsSplitter.widget(1)
        old.deleteLater()

        self.settingsWidget = selected[0].data(5, 6)()
        self.settingsSplitter.addWidget(self.settingsWidget)
        self.settingsWidget.masterRef = self.masterRef


class Appearance(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.masterRef = None

        self.ALayout = QGridLayout()
        btn = QLabel(Appearance.__name__)
        self.ALayout.addWidget(btn, 0, 0)

        self.spacer = QSpacerItem(50, 50)
        self.ALayout.addItem(self.spacer, 1, 0)
        self.autoSaveLbl = QLabel("Edits AutoSave Trigger")
        self.ALayout.addWidget(self.autoSaveLbl, 2, 1, alignment=Qt.AlignLeft)
        self.ALayout.setColumnMinimumWidth(0, 50)
        # self.ALayout.cellRect(2, 0).setWidth(self.autoSaveLbl.width())

        self.autoSaveTxt = QLineEdit()
        self.autoSaveTxt.setMaximumWidth(50)
        self.ALayout.addWidget(self.autoSaveTxt, 2, 2, 1, 10, alignment=Qt.AlignLeft)
        self.autoSaveTxt.editingFinished.connect(self.onSetAutoSave)
        print(self.ALayout.rowCount())

        self.setLayout(self.ALayout)
        self.layout().setAlignment(Qt.AlignTop)

    def onSetAutoSave(self):
        self.masterRef.onSetAutoSave(int(self.autoSaveTxt.text()))

class KeyMapping(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.masterRef = None

        lay = QVBoxLayout()
        self.setLayout(lay)

        btn = QLabel(KeyMapping.__name__)
        lay.addWidget(btn, 0, Qt.AlignTop)