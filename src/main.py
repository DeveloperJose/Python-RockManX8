import sentry_sdk
import sys

from app.app_manager import AppManager
from app.exception_manager import handle_exception

sys.excepthook = handle_exception

if __name__ == '__main__':
    sentry_sdk.init(dsn='https://9870efae765a4b1e9f876915cd8be37a@sentry.io/1497819')
    app_manager = AppManager()
    exit_code = app_manager.run()
    sys.exit(exit_code)
