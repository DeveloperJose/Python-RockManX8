@ECHO OFF
CALL activate pyqt5

CD src/gui/design
CALL pyuic5 main.ui -o ui_main.py
CALL pyuic5 texture_editor.ui -o ui_texture_editor.py
CALL pyuic5 text_editor.ui -o ui_text_editor.py
CALL pyuic5 character_map_dialog.ui -o ui_character_map.py
CD ../../..

ECHO Updated UI design Python code from .ui file
PAUSE
@ECHO ON