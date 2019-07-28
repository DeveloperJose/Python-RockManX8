@ECHO OFF
CALL activate pyqt5

CD src/gui/design
CALL pyuic5 editor_window.ui -o ui_editor_window.py
CALL pyuic5 character_map.ui -o ui_character_map.py
CD ../../..

ECHO Updated UI design Python code from .ui file
@ECHO ON