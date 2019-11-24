from PyQt5.QtCore import QTimer, QRegExp
from PyQt5.QtGui import QPixmap, QSyntaxHighlighter, QTextCharFormat, QColor, QIcon
from PyQt5.QtWidgets import QMainWindow

from PIL import Image
from PIL.ImageQt import ImageQt

from core.mcb import MCBFile, MCBExtra
import core.constants as Const

from gui.design.ui_editor_window import Ui_MainWindow
from gui.dialogues import CharacterMapDialog
from app import mcb_manager, resource_manager


class SyntaxHighligher(QSyntaxHighlighter):
    def __init__(self, parent):
        QSyntaxHighlighter.__init__(self, parent)
        self.parent = parent

        symbol_format = QTextCharFormat()
        symbol_format.setForeground(QColor(19, 150, 250))
        symbol_pattern = QRegExp(r"\[[0-9]+\]")
        symbol_pattern.setMinimal(True)

        self.formats = [symbol_format]
        self.patterns = [symbol_pattern]

    def highlightBlock(self, text):
        for frmt, pattern in zip(self.formats, self.patterns):
            idx = pattern.indexIn(text)

            while idx >= 0:
                length = pattern.matchedLength()
                self.setFormat(idx, length, frmt)
                idx = pattern.indexIn(text, idx + length)
        self.setCurrentBlockState(0)


class EditorWindow(QMainWindow):
    def __init__(self):
        super(EditorWindow, self).__init__(None)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowIcon(QIcon(resource_manager.resources.icon_path))
        self.__init_ui__()

    def __init_ui__(self):
        self.mcb = None
        self.char_map_dialog = CharacterMapDialog(self.evt_clicked_dialog_insert)

        self.__init_file_group__()
        self.__init_editor_group__()
        self.__init_extra_group__()
        self.__init_preview_group__()
        self.adjustSize()

    def __init_file_group__(self):
        for fname in mcb_manager.get_mcb_names():
            desc = MCBFile.get_filename_description(fname)
            self.ui.comboFiles.addItem(fname + ' - [' + desc + ']')

        self.ui.btnOpenCloseFile.clicked.connect(self.evt_clicked_openclosefile)

    def __init_editor_group__(self):
        self.ui.groupText.setVisible(False)
        self.ui.spinCurrentText.valueChanged.connect(lambda new_value: self.ui_update_editor())
        self.ui.textEditor.textChanged.connect(lambda: self.ui_update_preview())
        self.ui.textEditor.textChanged.connect(self.enable_save)
        self.syntax_highlighter = SyntaxHighligher(self.ui.textEditor)

        self.ui.btnOpenCharMap.clicked.connect(self.evt_clicked_opencharmap)
        self.ui.btnSave.clicked.connect(self.evt_clicked_save)
        self.ui.btnRevert.clicked.connect(lambda: self.ui_update_editor())

    def __init_extra_group__(self):
        self.ui.groupExtraData.setVisible(False)

        voices = [str(i) for i in range(818)]
        voices.append('None')
        self.ui.comboVoice.addItems(voices)

        bgms = [str(i) for i in range(61)]
        bgms.append('None')
        self.ui.comboBGM.addItems(bgms)

        self.ui.spinCameraAngle.setRange(0, 3)

        self.ui.comboCharacter.addItems(Const.CHARACTERS)
        self.ui.comboCharacter.currentIndexChanged.connect(self.ui_update_character)
        self.ui.spinMugshot.valueChanged.connect(self.ui_update_mugshot)

        self.ui.comboMugshotPos.addItems(['Left', 'Right'])
        self.ui.comboTextPos.addItems(['Top', 'Bottom'])

        self.ui.comboVoice.currentIndexChanged.connect(self.enable_save)
        self.ui.comboBGM.currentIndexChanged.connect(self.enable_save)
        self.ui.spinCameraAngle.valueChanged.connect(self.enable_save)
        self.ui.comboCharacter.currentIndexChanged.connect(self.enable_save)
        self.ui.spinMugshot.valueChanged.connect(self.enable_save)
        self.ui.comboMugshotPos.currentIndexChanged.connect(self.enable_save)
        self.ui.comboTextPos.currentIndexChanged.connect(self.enable_save)
        self.ui.checkArrow.stateChanged.connect(self.enable_save)
        self.ui.checkTyping.stateChanged.connect(self.enable_save)
        self.ui.checkCloseTop.stateChanged.connect(self.enable_save)
        self.ui.checkStopBGM.stateChanged.connect(self.enable_save)

    def __init_preview_group__(self):
        self.ui.groupPreview.setVisible(False)

    def get_current_extra(self):
        idx = self.ui.spinCurrentText.value()
        return self.mcb.extras[idx]

    def get_current_text_bytes(self):
        idx = self.ui.spinCurrentText.value()
        return self.mcb.texts_raw[idx]

    def get_current_mcb_name(self):
        mcb_name = self.ui.comboFiles.currentText().split('-')[0].strip()
        return mcb_name

    def enable_save(self, *args, **kwargs):
        self.ui.btnRevert.setEnabled(True)
        self.ui.btnSave.setEnabled(True)
        self.ui.btnSave.setText('Save Changes*')

    def disable_save(self):
        self.ui.btnRevert.setEnabled(False)
        self.ui.btnSave.setEnabled(False)
        self.ui.btnSave.setText('Save Changes')

    def evt_timer_redraw(self):
        self.adjustSize()

    def evt_clicked_dialog_insert(self, checked):
        char_byte = self.char_map_dialog.get_selected_char_byte()
        insert_str = f'[{char_byte}]'
        self.ui.textEditor.insertPlainText(insert_str)

    def evt_clicked_opencharmap(self, checked):
        self.char_map_dialog.show()

    def evt_clicked_openclosefile(self, checked):
        if self.mcb is None:
            self.ui_file_open()
        else:
            self.ui_file_close()

        # For proper resizing, you need to wait a little bit
        QTimer().singleShot(0, self.evt_timer_redraw)

    def evt_clicked_save(self, checked):
        # Convert text to bytes, then replace them in the MCB
        idx = self.ui.spinCurrentText.value()
        curr_text = self.ui.textEditor.toPlainText()
        curr_bytes = MCBFile.convert_text_to_bytes(curr_text)
        self.mcb.texts_raw[idx] = curr_bytes

        if self.mcb.has_extras():
            voice_name = self.ui.comboVoice.currentText()
            voice_idx = 0xFFFF if voice_name == 'None' else self.ui.comboVoice.currentIndex()

            bgm_name = self.ui.comboBGM.currentText()
            bgm_idx = 0xFFFF if bgm_name == 'None' else self.ui.comboBGM.currentIndex()

            char_name = self.ui.comboCharacter.currentText()
            char_idx = 0xFFFF if char_name == 'None' else self.ui.comboCharacter.currentIndex()

            camera_idx = 0xFFFF
            if self.ui.spinCameraAngle.isEnabled():
                camera_idx = self.ui.spinCameraAngle.value()

            # Note: Mugshot byte values start at 1, but indices start 0
            mugshot_idx = self.ui.spinMugshot.value() + 1

            mugshot_pos_idx = MCBExtra.MugshotPosition[self.ui.comboMugshotPos.currentText()]
            text_pos_idx = MCBExtra.TextPosition[self.ui.comboTextPos.currentText()].value

            close_top_idx = 0 if self.ui.checkCloseTop.isChecked() else 0xFFFF
            typing_idx = 0 if self.ui.checkTyping.isChecked() else 1
            show_arrow_idx = 1 if self.ui.checkArrow.isChecked() else 2
            stop_bgm_idx = 0 if self.ui.checkStopBGM.isChecked() else 0xFFFF

            # Special Case: Set to 1 when position is Top
            close_top_idx = 1 if text_pos_idx == MCBExtra.TextPosition.Top else close_top_idx

            extra = self.get_current_extra()
            extra.voice = voice_idx
            extra.bgm = bgm_idx
            extra.stop_bgm = stop_bgm_idx
            extra.camera_angle = camera_idx
            extra.char = char_idx
            extra.char_mug = mugshot_idx
            extra.char_mug_pos = mugshot_pos_idx
            extra.close_top = close_top_idx
            extra.text_pos = text_pos_idx
            extra.typing = typing_idx
            extra.show_arrow = show_arrow_idx

            self.mcb.extras[idx] = extra

        self.ui.statusbar.showMessage('Saving changes...', 5000)

        self.mcb.save()
        mcb_manager.update_collection_mcb(mcb_name=self.get_current_mcb_name())

        self.ui.statusbar.showMessage('Succesfully saved changes!', 5000)
        self.disable_save()

    def ui_file_open(self):
        self.ui.btnOpenCloseFile.setText("Close File")
        self.mcb = mcb_manager.get_mcb(mcb_name=self.get_current_mcb_name())

        self.ui.comboFiles.setDisabled(True)
        self.ui.groupText.setVisible(True)
        self.ui.groupPreview.setVisible(True)

        self.ui_update_editor()

    def ui_file_close(self):
        self.ui.btnOpenCloseFile.setText("Open File")
        self.mcb = None

        self.char_map_dialog.close()
        self.ui.comboFiles.setEnabled(True)
        self.ui.groupText.setVisible(False)
        self.ui.groupExtraData.setVisible(False)
        self.ui.groupPreview.setVisible(False)

    def ui_update_mugshot(self, mug_idx):
        # Update the mugshot text number and description
        char_idx = self.ui.comboCharacter.currentIndex()
        self.ui.spinMugshot.setValue(mug_idx)
        self.ui.textMugshotDesc.setText(MCBExtra.get_mugshot_description(char_idx, mug_idx))

        im = self.get_mugshot_im(char_idx, mug_idx)
        qt_im = ImageQt(im)
        pixmap = QPixmap.fromImage(qt_im)
        self.ui.graphicsMugshot.setPixmap(pixmap)

    def ui_update_character(self, char_idx):
        mugshots = Const.MUGSHOT_DESCRIPTIONS[char_idx]
        num_mugshots = len(mugshots)

        self.ui.comboCharacter.setCurrentIndex(char_idx)
        self.ui_update_mugshot(0)
        self.ui.spinMugshot.setRange(0, num_mugshots - 1)
        self.ui.spinMugshot.setDisabled(num_mugshots == 1)

    def ui_update_preview(self):
        curr_text = self.ui.textEditor.toPlainText()
        curr_bytes = MCBFile.convert_text_to_bytes(curr_text)

        im = resource_manager.resources.font.text_bytes_to_image(curr_bytes)
        qt_im = ImageQt(im)
        pixmap = QPixmap.fromImage(qt_im)
        if pixmap is not None:
            self.ui.graphicsPreview.setPixmap(pixmap)

    def ui_update_editor(self):
        if self.mcb is None:
            return

        idx = self.ui.spinCurrentText.value()

        # Text Counts
        total_texts = len(self.mcb.texts_raw) - 1
        self.ui.spinCurrentText.setRange(0, total_texts)
        if idx > total_texts:
            idx = 0
        self.ui.spinCurrentText.setValue(idx)
        self.ui.lblTotalTexts.setText(f'<span style=" color:#aa0000;">{total_texts}</span>')

        # Current Text
        text = MCBFile.convert_bytes_to_text(self.mcb.texts_raw[idx])
        self.ui.textEditor.setText(text)

        self.disable_save()
        self.ui_update_extra_data()

    def ui_update_extra_data(self):
        self.ui.groupExtraData.setVisible(self.mcb.has_extras())
        self.ui.graphicsMugshot.setVisible(self.mcb.has_extras())
        if not self.mcb.has_extras():
            return

        extra = self.get_current_extra()
        voice_idx = extra.voice if extra.voice != 0xFFFF else self.ui.comboVoice.findText('None')
        bgm_idx = extra.bgm if extra.bgm != 0xFFFF else self.ui.comboBGM.findText('None')
        char_idx = extra.char if extra.char != 0xFFFF else self.ui.comboCharacter.findText('None')
        text_pos_idx = extra.text_pos if extra.text_pos == 1 else 0

        self.ui.textFilename.setText(extra.filename)
        self.ui.comboVoice.setCurrentIndex(voice_idx)
        self.ui.comboBGM.setCurrentIndex(bgm_idx)
        self.ui.comboMugshotPos.setCurrentIndex(extra.char_mug_pos)
        self.ui.comboTextPos.setCurrentIndex(text_pos_idx)

        self.ui.checkCloseTop.setChecked(extra.close_top == 0)
        self.ui.checkTyping.setChecked(extra.typing == 0)
        self.ui.checkArrow.setChecked(extra.show_arrow == 1)
        self.ui.checkStopBGM.setChecked(extra.stop_bgm == 0)

        self.ui_update_character(char_idx)
        self.ui_update_mugshot(extra.char_mug - 1)

        is_camera_disabled = (extra.camera_angle == 0xFFFF)
        self.ui.spinCameraAngle.setDisabled(is_camera_disabled)
        if is_camera_disabled:
            self.ui.spinCameraAngle.setSpecialValueText('N/A')
        else:
            self.ui.spinCameraAngle.setValue(extra.camera_angle)

        self.disable_save()

    @staticmethod
    def get_mugshot_im(char_idx, mug_idx):
        if not MCBExtra.is_valid_char(char_idx):
            return Image.new("RGB", (128, 128))

        curr_mugshots = resource_manager.resources.mugshots[char_idx]
        is_valid_mugshot = (0 <= mug_idx < len(curr_mugshots))
        if not is_valid_mugshot:
            return Image.new("RGB", (128, 128))

        return curr_mugshots[mug_idx]
