import os
from typing import List

import numpy as np
import qimage2ndarray
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QMainWindow

from editor_v2 import Ui_MainWindow
from x8_utils import Const, MCBFile, MCBExtra, Font


def safe_run(func):
    def func_wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            print(e)
            return None

    return func_wrapper


class EditorWindow(QMainWindow):
    installation_path: str
    language: str
    mcb_folder_path: str
    font_path: str

    mcb: MCBFile
    font: Font
    mcb_files: List[str]

    def __init__(self, installation_path, language):
        super(EditorWindow, self).__init__(None)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.installation_path = installation_path
        self.language = language

        self.font_path = os.path.join('opk', 'title', language, 'wpg', 'font_ID_FONT_000.wpg')
        self.mcb_folder_path = os.path.join(installation_path, 'mes', language)

        self.mcb = None
        self.font = Font(self.font_path)
        self.mcb_files = os.listdir(self.mcb_folder_path)

        self.__init_file_group__()
        self.__init_editor_group__()
        self.__init_extra_group__()
        self.__init_preview_group__()

    def __init_file_group__(self):
        for fname in self.mcb_files:
            desc = MCBFile.get_filename_description(fname)
            self.ui.comboFiles.addItem(fname + ' - [' + desc + ']')

        self.ui.btnOpenCloseFile.clicked.connect(self.clicked_openclosefile)

    def __init_editor_group__(self):
        self.ui.groupText.setVisible(False)
        self.ui.spinCurrentText.valueChanged.connect(self.ui_update_editor)

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

    def __init_preview_group__(self):
        self.ui.groupPreview.setVisible(False)

    def get_current_extra(self):
        idx = self.ui.spinCurrentText.value()
        return self.mcb.extras[idx]

    def get_current_text_bytes(self):
        idx = self.ui.spinCurrentText.value()
        return self.mcb.texts_raw[idx]

    def clicked_openclosefile(self, checked):
        if self.mcb is None:
            self.ui_file_open()
        else:
            self.ui_file_close()

    @safe_run
    def ui_file_open(self):
        self.ui.btnOpenCloseFile.setText("Close File")

        mcb_filename = self.ui.comboFiles.currentText().split('-')[0].strip()
        mcb_path = os.path.join(self.mcb_folder_path, mcb_filename)
        self.mcb = MCBFile(mcb_path)

        self.ui.comboFiles.setDisabled(True)
        self.ui.groupText.setVisible(True)
        self.ui.groupPreview.setVisible(True)

        self.ui_update_editor()
        self.ui_update_extra_data()

    def ui_file_close(self):
        self.ui.btnOpenCloseFile.setText("Open File")
        self.mcb = None

        self.ui.comboFiles.setEnabled(True)
        self.ui.groupText.setVisible(False)
        self.ui.groupExtraData.setVisible(False)
        self.ui.groupPreview.setVisible(False)

    @safe_run
    def ui_update_mugshot(self, mug_idx):
        extra = self.get_current_extra()
        # Update the mugshot text number and description
        char_idx = self.ui.comboCharacter.currentIndex()
        self.ui.spinMugshot.setValue(mug_idx)
        self.ui.textMugshotDesc.setText(MCBExtra.get_mugshot_description(char_idx, mug_idx))

    @safe_run
    def ui_update_character(self, char_idx):
        mugshots = Const.MUGSHOT_DESCRIPTIONS[char_idx]
        num_mugshots = len(mugshots)

        self.ui.comboCharacter.setCurrentIndex(char_idx)
        self.ui_update_mugshot(0)
        self.ui.spinMugshot.setRange(0, num_mugshots - 1)
        self.ui.spinMugshot.setDisabled(num_mugshots==1)

    def ui_update_preview(self):
        curr_text = self.ui.textEditor.toPlainText()
        curr_bytes = MCBFile.convert_text_to_bytes(curr_text)

        im_text = self.text_bytes_to_np(curr_bytes)
        self.ui.graphicsPreview.setPixmap(self.np_to_pixmap(im_text))

    @safe_run
    def ui_update_editor(self, idx=None):
        if self.mcb is None:
            return

        if idx is None:
            idx = self.ui.spinCurrentText.value()

        # Text Counts
        total_texts = len(self.mcb.texts_raw) - 1
        self.ui.spinCurrentText.setRange(0, total_texts)
        self.ui.spinCurrentText.setValue(idx)
        self.ui.lblTotalTexts.setText('<span style=" font-size:12pt; color:#aa0000;">{}</span>'.format(total_texts))

        # Current Text
        text = MCBFile.convert_bytes_to_text(self.mcb.texts_raw[idx])
        self.ui.textEditor.setText(text)

    @safe_run
    def ui_update_extra_data(self):
        self.ui.groupExtraData.setVisible(self.mcb.has_extras())
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
            self.ui.spinCameraAngle.setSpecialValueText('Disabled')
        else:
            self.ui.spinCameraAngle.setValue(extra.camera_angle)

    @safe_run
    def np_to_pixmap(self, arr: np.ndarray):
        q_im = qimage2ndarray.array2qimage(arr)
        return QPixmap(q_im)

    @safe_run
    def text_bytes_to_np(self, raw_bytes):
        split_indices = [0]
        split_indices.extend([idx + 1 for idx, char_byte in enumerate(raw_bytes) if char_byte == 65533])
        split_indices.append(len(raw_bytes) + 1)
        sentences = []
        max_sentence_char = 0
        for split_idx, slice_start in enumerate(split_indices):
            if split_idx >= len(split_indices) - 1:
                break
            slice_end = split_indices[split_idx + 1]
            sentence = raw_bytes[slice_start:slice_end]
            max_sentence_char = max(max_sentence_char, len(sentence))
            sentences.append(sentence)

        cols = 20 * max_sentence_char
        rows = 20 * len(sentences)
        im = np.zeros((rows, cols))
        for row_idx, sentence in enumerate(sentences):
            row_start = row_idx * 20
            row_end = row_start + 20
            for col_idx, char_byte in enumerate(sentence):
                if char_byte >= len(self.font.characters):
                    im_curr_char = self.font.characters[0]
                else:
                    im_curr_char = self.font.characters[char_byte]
                col_start = col_idx * 20
                col_end = col_start + 20
                im[row_start:row_end, col_start:col_end] = im_curr_char

        return im