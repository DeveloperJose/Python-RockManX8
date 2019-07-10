from fbs_runtime import platform
from fbs_runtime.application_context import cached_property
from fbs_runtime.application_context.PyQt5 import ApplicationContext
from fbs_runtime.excepthook import ExceptionHandler
from fbs_runtime.excepthook.sentry import SentryExceptionHandler

from ui_editor_window import EditorWindow


class AppContext(ApplicationContext):
    editor: EditorWindow

    @property
    def ui(self):
        return self.editor.ui

    def run(self):
        pass

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
        return SentryExceptionHandler(dns, ver, env, callback=self._on_sentry_init)

    @cached_property
    def _on_sentry_init(self):
        self.sentry.scope.set_extra('os', platform.name())

        if self.editor is not None:
            self.sentry.scope.set_extra('X8 Language', self.editor.language)

            mcb = self.editor.mcb
            if mcb is not None:
                idx = self.ui.spinCurrentText.value()
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
        if self.ui is not None:
            msg = "{}".format(exc_value)
            self.app_context.ui.statusbar.showMessage(msg, 30000)
