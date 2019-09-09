# Python-RockManX8 Overview
This is a set of scripts and applications that allow you to modify several aspects of Mega Man X8 (2004 PC version and X Legacy Collection 2 version). Currently, only text editing is fully supported.

# Getting Started
If you have a 64-bit Windows machine, you can download the pre-bundled package from ...

## Requirements
* Python >= 3.7
* PyQt5 >= 5.13
* numpy >= 1.17 (to extract the characters from the font WPG files)
* Pillow >= 6.1 (to load images for use with numpy)
* qimage2ndarray >= 1.8 (used to convert numpy arrays to qimages for PyQt)
* sentry-sdk >= 0.10.2 (error tracking)

### Optional Requirements
* PyQt5-Tools >= 5.11.3 (if you plan to update the QT Designer .ui files)
* PyInstaller >= 3.5 (if you plan on bundling the package into one executable)

## Running (from source)
Clone this repository using git, then run *"gui/main.py"*

# License
The MIT License (see LICENSE)


# Acknowledgments
* ARCtool by FluffyQuack (v0.9.428) which allowed for editing on the X Legacy Collection 2