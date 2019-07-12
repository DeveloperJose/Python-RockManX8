import sys

from PyQt5.QtWidgets import QApplication

from fbs_utils import AppContext

if __name__ == '__main__':
    app = QApplication([])
    appctxt = AppContext()
    exit_code = appctxt.run()
    sys.exit(exit_code)
