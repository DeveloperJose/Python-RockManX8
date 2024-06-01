from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow

from app import resource_manager
from gui.design.ui_main import Ui_MainWindow


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__(None)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowIcon(QIcon(resource_manager.resources.icon_path))

        self.setWindowTitle("Main")
        self.ui.uxBtnTextEditor.clicked.connect(self.openLevelEditor)
        self.ui.uxBtnTextureEditor.clicked.connect(self.openLevelEditor)
        self.ui.uxBtnLevelEditor.clicked.connect(self.openLevelEditor)

    def openLevelEditor(self):
        pass