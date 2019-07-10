import os
import subprocess
from configparser import ConfigParser

import numpy as np
import qimage2ndarray
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QMainWindow, QProgressDialog

import fbs_utils as fbs
import shutil
from ui_design import Ui_MainWindow
from x8_utils import Const, MCBFile, MCBExtra, Font


class MCBManager:
    font: Font

    @staticmethod
    def mcb_sorting_key(fname: str):
        key = len(fname)
        if 'TRIAL' in fname:
            key += 1
        if '_' in fname:
            key += 2
        if 'DM' in fname:
            key += 3
        if 'ST' in fname:
            key += 4
        if 'VA' in fname:
            key += 5
        if 'MOV' in fname:
            key += 6

        return key

    def __init__(self, appctxt, config: ConfigParser):
        self.appctxt = appctxt
        self.config = config

        self.is_valid_collection = config.getboolean('editor', 'is_legacy_collection')
        self.language = config['editor']['language']
        self.install_path = config['editor']['installation_path']

        self.font_path = appctxt.get_resource('font.wpg')
        self.arctool_path = appctxt.get_resource('arctool.exe')

        if self.is_valid_collection:
            self.mcb_path = os.path.join('ARC')
            self.extract_arcs()
        else:
            self.font_path = os.path.join(self.install_path, 'opk', 'title', self.language.lower(), 'wpg', 'font_ID_FONT_000.wpg')
            self.mcb_path = os.path.join(self.install_path, 'mes', self.language)

        self.font = Font(self.font_path)

    def extract_arcs(self):
        if not self.is_valid_collection:
            return

        if os.path.exists(self.mcb_path):
            return

        diag = QProgressDialog("Processing Legacy Collection ARC Files", "Cancel", 0, 110)
        diag.setModal(True)

        arc_path = os.path.join(self.install_path, 'nativeDX10', 'X8', 'romPC', 'data', 'mes', self.language)
        for idx, fname in enumerate(os.listdir(arc_path)):
            diag.setValue(idx)
            fpath = os.path.join(arc_path, fname)
            subprocess.call([self.arctool_path, '-x', '-pc', '-noextractdir', fpath])

        src = os.path.join(arc_path, 'X8', 'data', 'mes', 'USA')
        dst = self.mcb_path
        shutil.move(src, dst)
        shutil.rmtree(os.path.join(arc_path, 'X8'))

    def update_arcs(self):
        if not self.is_valid_collection:
            return

    def get_mcb_files(self):
        return sorted(os.listdir(self.mcb_path), key=self.mcb_sorting_key)


class EditorWindow(QMainWindow):
    mcbManager: MCBManager
    mcb: MCBFile

    def __init__(self, appctxt, config):
        super(EditorWindow, self).__init__(None)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.appctxt = appctxt
        self.config = config
        self.mcbManager = MCBManager(appctxt, config)
        self.mcb = None

        self.__init_file_group__()
        self.__init_editor_group__()
        self.__init_extra_group__()
        self.__init_preview_group__()
        self.adjustSize()

    def __init_file_group__(self):
        for fname in self.mcbManager.get_mcb_files():
            desc = MCBFile.get_filename_description(fname)
            self.ui.comboFiles.addItem(fname + ' - [' + desc + ']')

        self.ui.btnOpenCloseFile.clicked.connect(self.evt_clicked_openclosefile)

    def __init_editor_group__(self):
        self.ui.groupText.setVisible(False)
        self.ui.spinCurrentText.valueChanged.connect(lambda new_value: self.ui_update_editor())
        self.ui.textEditor.textChanged.connect(lambda: self.ui_update_preview())
        self.ui.textEditor.textChanged.connect(self.enable_save)

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

    def enable_save(self, *args, **kwargs):
        self.ui.btnSave.setEnabled(True)
        self.ui.btnSave.setText('Save Changes*')

    def disable_save(self):
        self.ui.btnSave.setEnabled(False)
        self.ui.btnSave.setText('Save Changes')

    def evt_timer_redraw(self):
        self.adjustSize()

    def evt_clicked_openclosefile(self, checked):
        if self.mcb is None:
            self.ui_file_open()
        else:
            self.ui_file_close()

        # For proper resizing, you need to wait a little bit
        QTimer.singleShot(0, self.evt_timer_redraw)

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

        self.mcb.save()
        self.mcbManager.update_arcs()
        self.ui.statusbar.showMessage('Saved MCB changes!', 5000)
        self.disable_save()

    def ui_file_open(self):
        self.ui.btnOpenCloseFile.setText("Close File")

        mcb_filename = self.ui.comboFiles.currentText().split('-')[0].strip()
        mcb_path = os.path.join(self.mcbManager.mcb_path, mcb_filename)
        self.mcb = MCBFile(mcb_path)

        self.ui.comboFiles.setDisabled(True)
        self.ui.groupText.setVisible(True)
        self.ui.groupPreview.setVisible(True)

        self.ui_update_editor()

    def ui_file_close(self):
        self.ui.btnOpenCloseFile.setText("Open File")
        self.mcb = None

        self.ui.comboFiles.setEnabled(True)
        self.ui.groupText.setVisible(False)
        self.ui.groupExtraData.setVisible(False)
        self.ui.groupPreview.setVisible(False)

    def ui_update_mugshot(self, mug_idx):
        extra = self.get_current_extra()
        # Update the mugshot text number and description
        char_idx = self.ui.comboCharacter.currentIndex()
        self.ui.spinMugshot.setValue(mug_idx)
        self.ui.textMugshotDesc.setText(MCBExtra.get_mugshot_description(char_idx, mug_idx))

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

        im_text = self.text_bytes_to_np(curr_bytes)
        q_im = qimage2ndarray.array2qimage(im_text)
        pixmap = QPixmap(q_im)
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
        self.ui.lblTotalTexts.setText('<span style=" color:#aa0000;">{}</span>'.format(total_texts))

        # Current Text
        text = MCBFile.convert_bytes_to_text(self.mcb.texts_raw[idx])
        self.ui.textEditor.setText(text)

        self.disable_save()
        self.ui_update_extra_data()

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
            self.ui.spinCameraAngle.setSpecialValueText('N/A')
        else:
            self.ui.spinCameraAngle.setValue(extra.camera_angle)

        self.disable_save()

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
        font = self.mcbManager.font
        for row_idx, sentence in enumerate(sentences):
            row_start = row_idx * 20
            row_end = row_start + 20
            for col_idx, char_byte in enumerate(sentence):
                if char_byte >= len(font.characters):
                    im_curr_char = font.characters[0]
                else:
                    im_curr_char = font.characters[char_byte]
                col_start = col_idx * 20
                col_end = col_start + 20
                im[row_start:row_end, col_start:col_end] = im_curr_char

        return im
