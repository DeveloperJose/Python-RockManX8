import sys

from app.app_manager import AppManager
from app.exception_manager import handle_exception

sys.excepthook = handle_exception

if __name__ == "__main__":
    app_manager = AppManager()
    exit_code = app_manager.run()
    sys.exit(exit_code)
