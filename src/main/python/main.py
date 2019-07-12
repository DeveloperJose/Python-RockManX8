import sys

from fbs_utils import AppContext
from PyQt5.QtWidgets import QApplication

if __name__ == '__main__':
    app = QApplication([])
    appctxt = AppContext()
    exit_code = appctxt.run()
    sys.exit(exit_code)