import PyQt5
from dialog_editor import Ui_MainWindow  # importing our generated file
from mcb_editor import Ui_MCBWidget
import sys

class mywindow(PyQt5.QtWidgets.QMainWindow):
    def action_open(self):
        print("yay")

    def __init__(self):
        super(mywindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.actionOpen_X8_Text_File.triggered.connect(self.action_open)

app = PyQt5.QtWidgets.QApplication([])
application = mywindow()
application.show()
sys.exit(app.exec())