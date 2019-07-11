from fbs_runtime import platform
from fbs_runtime.application_context import cached_property
from fbs_runtime.application_context.PyQt5 import ApplicationContext
from fbs_runtime.excepthook import ExceptionHandler
from fbs_runtime.excepthook.sentry import SentryExceptionHandler

from config_utils import Config
from ui_editor_window import EditorWindow
from PyQt5.QtWidgets import QMessageBox


class AppContext(ApplicationContext):
    config: Config
    __editor__: EditorWindow

    def log(self, message, *args):
        message = message.format(*args)
        print('[RainLog]', message)

    def log_ui(self, message, *args, duration_ms=1000):
        if self.__editor__ is None:
            return

        message = message.format(*args)
        self.__editor__.ui.statusbar.showMessage(message, duration_ms)

    @cached_property
    def exception_handlers(self):
        result = super().exception_handlers
        result.append(UIExceptionHandler(self))

        # if is_frozen():
        # result.append(self.sentry_exception_handler)
        return result

    @cached_property
    def sentry(self):
        dns = self.build_settings['sentry_dsn']
        ver = self.build_settings['version']
        env = self.build_settings['environment']
        return SentryExceptionHandler(dns, ver, env, callback=self._on_sentry_init, rate_limit=10)

    @cached_property
    def _on_sentry_init(self):
        self.sentry.scope.set_extra('os', platform.name())

        if self.__editor__ is not None:
            self.sentry.scope.set_extra('X8 Language', self.__editor__.language)

            mcb = self.__editor__.mcb
            if mcb is not None:
                idx = self.__editor__.ui.spinCurrentText.value()
                self.sentry.scope.set_extra('MCB IDX', idx)
                self.sentry.scope.set_extra('MCB Path', mcb.path)
                self.sentry.scope.set_extra('MCB Text Bytes', mcb.texts_raw[idx])

                if mcb.has_extras():
                    self.sentry.scope.set_extra('MCB Extra Bytes', mcb.extras[idx])
        return self.sentry

    def run(self):
        pass


class UIExceptionHandler(ExceptionHandler):
    app_context: AppContext = None

    def __init__(self, app_context):
        self.app_context = app_context

    def handle(self, exc_type, exc_value, enriched_tb):
        if self.app_context.__editor__ is None:
            return

        # self.app_context.log_ui('{}', exc_value, 15000)
        mbox = QMessageBox(self.app_context.__editor__)
        mbox.setModal(True)
        mbox.setIcon(QMessageBox.Warning)
        mbox.setWindowTitle('An error has occurred! [uh-oh?]')

        if isinstance(exc_value, PermissionError):
            msg = 'Permission denied while trying to write to file: {}'.format(exc_value.filename)
            info = 'That file is most likely read-only. Please make sure to disable that on the file/folder properties and trying again!'
        else:
            msg = 'Error: {}'.format(exc_value)
            info = 'An unknown error has occured. RainfallPianist has been sent the error information and may be able to provide assistance.'

        mbox.setText(msg)
        mbox.setInformativeText(info)
        mbox.setDetailedText(str(enriched_tb))
        mbox.show()