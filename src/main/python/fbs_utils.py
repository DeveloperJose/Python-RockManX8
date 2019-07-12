from pathlib import Path

from PyQt5.QtWidgets import QFileDialog, QInputDialog
from PyQt5.QtWidgets import QMessageBox
from fbs_runtime import platform
from fbs_runtime.application_context import cached_property, is_frozen
from fbs_runtime.application_context.PyQt5 import ApplicationContext
from fbs_runtime.excepthook import ExceptionHandler
from fbs_runtime.excepthook.sentry import SentryExceptionHandler

from config_utils import Config
from ui_editor_window import EditorWindow

LANGUAGES = ['SPA - [Spanish]', 'USA - [English (USA)]', 'ENG - [English (Europe)]', 'CHI - [Chinese]', 'FRE - [French]', 'GER - [German]', 'ITA - [Italian]', 'JPN - [Japanese]', 'KOR - [Korean]']
SETTINGS_PATH = Path('settings.ini')


class AppContext(ApplicationContext):

    @cached_property
    def __editor__(self) -> EditorWindow:
        editor_app = EditorWindow()
        editor_app.setWindowTitle('MegaManX8 Text Editor by RainfallPianist [{}]'.format(self.build_settings['version']))
        return editor_app

    @cached_property
    def config(self) -> Config:
        if SETTINGS_PATH.exists():
            cfg = Config.from_path(SETTINGS_PATH)
        else:
            install_path = self.prompt_installation()
            if not install_path:
                return False

            lang_folder = self.prompt_language()
            if not lang_folder:
                return False

            is_valid_collection = (install_path / 'nativeDX10' / 'X8' / 'romPC' / 'data' / 'mes').exists()
            cfg = Config.create_default(SETTINGS_PATH, lang_folder, install_path, is_valid_collection)

        return cfg

    def run(self):
        if not self.config:
            return False

        self.__editor__.__init_ui__(self)
        self.__editor__.show()
        if self.config.is_valid_collection:
            self.log_ui('Editing X8 from the X Legacy Collection 2')
        else:
            self.log_ui('Editing X8 PC version released in 2004')

        return self.app.exec_()

    def log_ui(self, message, *args, duration_ms=5000):
        if self.__editor__ is None:
            return

        message = message.format(*args)
        self.__editor__.ui.statusbar.showMessage(message, duration_ms)

    @staticmethod
    def prompt_language():
        prompt, language_selected = QInputDialog.getItem(None, 'Language Select', 'Please select the language to edit'.ljust(50), LANGUAGES, 0, False)

        if language_selected:
            lang_folder = prompt.split('-')[0].strip()
            return lang_folder
        return False

    @staticmethod
    def prompt_installation():
        while True:
            install_fname = QFileDialog.getExistingDirectory(None, caption='Please select your X8 or Legacy Collection installation folder', directory='')
            if install_fname == '':
                return False

            install_path = Path(install_fname)
            regular_path = install_path / 'mes'
            collection_path = install_path / 'nativeDX10' / 'X8' / 'romPC' / 'data' / 'mes'
            if regular_path.exists() or collection_path.exists():
                return install_path

    @cached_property
    def exception_handlers(self):
        result = super().exception_handlers
        result.append(UIExceptionHandler(self))

        if is_frozen():
            result.append(self.sentry)
        return result

    @cached_property
    def sentry(self):
        dns = self.build_settings['sentry_dsn']
        ver = self.build_settings['version']
        env = self.build_settings['environment']
        return SentryExceptionHandler(dns, ver, env, callback=self._on_sentry_init, rate_limit=10)

    def _on_sentry_init(self):
        self.sentry.scope.set_extra('os', platform.name())

        if self.__editor__ is not None:
            self.sentry.scope.set_extra('X8 Language', self.config.language)
            self.sentry.scope.set_extra('Legacy Collection?', self.config.is_valid_collection)

            mcb = self.__editor__.mcb
            if mcb is not None:
                idx = self.__editor__.ui.spinCurrentText.value()
                self.sentry.scope.set_extra('MCB IDX', idx)
                self.sentry.scope.set_extra('MCB Path', mcb.path)
                self.sentry.scope.set_extra('MCB Text Bytes', mcb.texts_raw[idx])

                if mcb.has_extras():
                    self.sentry.scope.set_extra('MCB Extra Bytes', mcb.extras[idx])


class UIExceptionHandler(ExceptionHandler):
    app_context: AppContext = None

    def __init__(self, app_context):
        self.app_context = app_context

    def handle(self, exc_type, exc_value, enriched_tb):
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
