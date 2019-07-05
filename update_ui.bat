@ECHO OFF
CD src/main/python

pyuic5 ui_design.ui -o ui_design.py

CD ../../..
ECHO Updated UI design Python code from .ui file
@ECHO ON