@ECHO OFF
CD src/main/python

activate fbs
pyuic5 ui_design.ui -o ui_design.py
pyuic5 ui_character_map.ui -o ui_character_map.py

CD ../../..
ECHO Updated UI design Python code from .ui file
@ECHO ON