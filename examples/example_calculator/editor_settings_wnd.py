from PyQt5 import *

from examples.example_calculator.master_window import *
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

        self.settingsTree = QTreeWidget()
        self.settingsTree.header().hide()
        self.settingsTree.setMaximumWidth(250)
        self.settingsTree.setMinimumWidth(150)
        self.settingsSplitter.addWidget(self.settingsTree)

        for Item in self.settingsList:
            self.Setting = QTreeWidgetItem([Item[0]])
            self.Setting.setData(5, 6, Item[1])
            self.settingsTree.addTopLevelItem(self.Setting)

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

        self.Appearance_Layout = QGridLayout()
        self.AppearanceWnd_Name = QLabel(Appearance.__name__)
        self.Appearance_Layout.addWidget(self.AppearanceWnd_Name, 0, 0)

        self.spacer = QSpacerItem(50, 50)
        self.Appearance_Layout.addItem(self.spacer, 1, 0)

        # Edits AutoSave Trigger
        self.autoSaveLbl = QLabel("Edits AutoSave Trigger")
        self.Appearance_Layout.addWidget(self.autoSaveLbl, 2, 1, alignment=Qt.AlignLeft)
        self.Appearance_Layout.setColumnMinimumWidth(0, 50)

        self.autoSaveTxt = QLineEdit()
        self.Appearance_Layout.addWidget(self.autoSaveTxt, 2, 2, 1, 10, alignment=Qt.AlignLeft)
        self.autoSaveTxt.setMaximumWidth(50)
        self.autoSaveTxt.editingFinished.connect(self.onSetAutoSave)

        self.setLayout(self.Appearance_Layout)
        self.layout().setAlignment(Qt.AlignTop)

    def onSetAutoSave(self):
        self.masterRef.autoSaveVar = int(self.autoSaveTxt.text())

class KeyMapping(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.masterRef = None

        self.KeyMapping_Layout = QGridLayout()
        self.KeyMappingWnd_Name = QLabel(KeyMapping.__name__)
        self.KeyMapping_Layout.addWidget(self.KeyMappingWnd_Name, 0, 0)

        self.spacer = QSpacerItem(50, 50)
        self.KeyMapping_Layout.addItem(self.spacer, 1, 0)

        self.settingslist = ["New Graph", "Open", "Set Project Location", "Save", "Save As", "Exit",
                             "Undo", "Redo", "Cut", "Copy", "Paste", "Delete"]

        for item in self.settingslist:
            lbl = QLabel(item)
            self.KeyMapping_Layout.addWidget(lbl, self.settingslist.index(item)+2, 1, alignment=Qt.AlignRight)
            self.KeyMapping_Layout.setColumnMinimumWidth(0, 50)

            KeySequence = QKeySequenceEdit()
            self.KeyMapping_Layout.addWidget(KeySequence, self.settingslist.index(item)+2, 2, 1, 10, alignment=Qt.AlignLeft)
            KeySequence.setMaximumWidth(100)

        # File Shortcuts
        self.KeyMapping_Layout.itemAtPosition(self.settingslist.index("New Graph")+2, 2).widget().editingFinished.connect(self.onSetNewGraph)
        self.KeyMapping_Layout.itemAtPosition(self.settingslist.index("Open")+2, 2).widget().editingFinished.connect(self.onSetOpen)
        self.KeyMapping_Layout.itemAtPosition(self.settingslist.index("Set Project Location")+2, 2).widget().editingFinished.connect(self.onSetProjectDir)
        self.KeyMapping_Layout.itemAtPosition(self.settingslist.index("Save")+2, 2).widget().editingFinished.connect(self.onSetSave)
        self.KeyMapping_Layout.itemAtPosition(self.settingslist.index("Save As")+2, 2).widget().editingFinished.connect(self.onSetSaveAs)
        self.KeyMapping_Layout.itemAtPosition(self.settingslist.index("Exit")+2, 2).widget().editingFinished.connect(self.onSetExit)

        # Edit Shortcuts
        self.KeyMapping_Layout.itemAtPosition(self.settingslist.index("Undo") + 2, 2).widget().editingFinished.connect(self.onSetUndo)
        self.KeyMapping_Layout.itemAtPosition(self.settingslist.index("Redo") + 2, 2).widget().editingFinished.connect(self.onSetRedo)
        self.KeyMapping_Layout.itemAtPosition(self.settingslist.index("Cut") + 2, 2).widget().editingFinished.connect(self.onSetCut)
        self.KeyMapping_Layout.itemAtPosition(self.settingslist.index("Copy") + 2, 2).widget().editingFinished.connect(self.onSetCopy)
        self.KeyMapping_Layout.itemAtPosition(self.settingslist.index("Paste") + 2, 2).widget().editingFinished.connect(self.onSetPaste)
        self.KeyMapping_Layout.itemAtPosition(self.settingslist.index("Delete") + 2, 2).widget().editingFinished.connect(self.onSetDelete)

        self.setLayout(self.KeyMapping_Layout)
        self.layout().setAlignment(Qt.AlignTop)

    # File Shortcuts
    def onSetNewGraph(self):
        index = self.settingslist.index("New Graph")
        self.masterRef.NewGraph = self.KeyMapping_Layout.itemAtPosition(index + 2, 2).widget().keySequence()

        self.masterRef.fileMenu.removeAction(self.masterRef.actNew)
        self.masterRef.actNew.setShortcut(self.masterRef.NewGraph)
        self.masterRef.fileMenu.insertAction(self.masterRef.actOpen, self.masterRef.actNew)

    def onSetOpen(self):
        index = self.settingslist.index("Open")
        self.masterRef.Open = self.KeyMapping_Layout.itemAtPosition(index + 2, 2).widget().keySequence()

        self.masterRef.fileMenu.removeAction(self.masterRef.actOpen)
        self.masterRef.actOpen.setShortcut(self.masterRef.Open)
        self.masterRef.fileMenu.insertAction(self.masterRef.actSetProjectDir, self.masterRef.actOpen)

    def onSetProjectDir(self):
        index = self.settingslist.index("Set Project Location")
        self.masterRef.setProjectDir = self.KeyMapping_Layout.itemAtPosition(index + 2, 2).widget().keySequence()

        self.masterRef.fileMenu.removeAction(self.masterRef.actSetProjectDir)
        self.masterRef.actSetProjectDir.setShortcut(self.masterRef.setProjectDir)
        self.masterRef.fileMenu.insertAction(self.masterRef.actSave, self.masterRef.actSetProjectDir)

    def onSetSave(self):
        index = self.settingslist.index("Save")
        self.masterRef.save = self.KeyMapping_Layout.itemAtPosition(index + 2, 2).widget().keySequence()

        self.masterRef.fileMenu.removeAction(self.masterRef.actSave)
        self.masterRef.actSave.setShortcut(self.masterRef.save)
        self.masterRef.fileMenu.insertAction(self.masterRef.actSaveAs, self.masterRef.actSave)

    def onSetSaveAs(self):
        index = self.settingslist.index("Save As")
        self.masterRef.SaveAs = self.KeyMapping_Layout.itemAtPosition(index + 2, 2).widget().keySequence()

        self.masterRef.fileMenu.removeAction(self.masterRef.actSaveAs)
        self.masterRef.actSaveAs.setShortcut(self.masterRef.SaveAs)
        self.masterRef.fileMenu.insertAction(self.masterRef.actExit, self.masterRef.actSaveAs)

    def onSetExit(self):
        index = self.settingslist.index("Exit")
        self.masterRef.Exit = self.KeyMapping_Layout.itemAtPosition(index + 2, 2).widget().keySequence()

        self.masterRef.fileMenu.removeAction(self.masterRef.actExit)
        self.masterRef.actExit.setShortcut(self.masterRef.Exit)
        self.masterRef.fileMenu.addAction(self.masterRef.actExit)

    # Edit Shortcuts
    def onSetUndo(self):
        index = self.settingslist.index("Undo")
        self.masterRef.Undo = self.KeyMapping_Layout.itemAtPosition(index + 2, 2).widget().keySequence()

        self.masterRef.editMenu.removeAction(self.masterRef.actUndo)
        self.masterRef.actUndo.setShortcut(self.masterRef.Undo)
        self.masterRef.editMenu.insertAction(self.masterRef.actRedo, self.masterRef.actUndo)

    def onSetRedo(self):
        index = self.settingslist.index("Redo")
        self.masterRef.Redo = self.KeyMapping_Layout.itemAtPosition(index + 2, 2).widget().keySequence()

        self.masterRef.editMenu.removeAction(self.masterRef.actRedo)
        self.masterRef.actRedo.setShortcut(self.masterRef.Redo)
        self.masterRef.editMenu.insertAction(self.masterRef.actCut, self.masterRef.actRedo)

    def onSetCut(self):
        index = self.settingslist.index("Cut")
        self.masterRef.Cut = self.KeyMapping_Layout.itemAtPosition(index + 2, 2).widget().keySequence()

        self.masterRef.editMenu.removeAction(self.masterRef.actCut)
        self.masterRef.actCut.setShortcut(self.masterRef.Cut)
        self.masterRef.editMenu.insertAction(self.masterRef.actCopy, self.masterRef.actCut)

    def onSetCopy(self):
        index = self.settingslist.index("Copy")
        self.masterRef.Copy = self.KeyMapping_Layout.itemAtPosition(index + 2, 2).widget().keySequence()

        self.masterRef.editMenu.removeAction(self.masterRef.actCopy)
        self.masterRef.actCopy.setShortcut(self.masterRef.Copy)
        self.masterRef.editMenu.insertAction(self.masterRef.actPaste, self.masterRef.actCopy)

    def onSetPaste(self):
        index = self.settingslist.index("Paste")
        self.masterRef.Paste = self.KeyMapping_Layout.itemAtPosition(index + 2, 2).widget().keySequence()

        self.masterRef.editMenu.removeAction(self.masterRef.actPaste)
        self.masterRef.actPaste.setShortcut(self.masterRef.Paste)
        self.masterRef.editMenu.insertAction(self.masterRef.actDelete, self.masterRef.actPaste)

    def onSetDelete(self):
        index = self.settingslist.index("Delete")
        self.masterRef.Delete = self.KeyMapping_Layout.itemAtPosition(index + 2, 2).widget().keySequence()

        self.masterRef.editMenu.removeAction(self.masterRef.actDelete)
        self.masterRef.actDelete.setShortcut(self.masterRef.Delete)
        self.masterRef.editMenu.addAction(self.masterRef.actDelete)