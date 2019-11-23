# Python-RockManX8: Mega Man X8 scripts and editors
This is a set of scripts and applications that allow you to modify several aspects of Mega Man X8 (2004 PC version and X Legacy Collection 2 version). 

Currently, only **text editing** is fully supported. 

## Mega Man X8 Text Editor
![Image of the user interface](/screenshot_text_editor.JPG)
![Image of an edit on X Legacy Collection 2 for PC](/screenshot_legacy.JPG)
![Image of an edit on the 2004 PC edition](/screenshot_regular.JPG)
Edit all dialog and text in the game!

[![Download the Text Editor](https://img.shields.io/badge/dynamic/json.svg?label=download&url=https://api.github.com/repos/rainfallpianist/Python-RockManX8/releases/latest&query=$.assets%5B0%5D.name)]

If you have a 64-bit Windows machine, you can download the pre-bundled package from the releases tab or the button above.

Supports both the 2004 PC Version and the X Legacy Collection 2 Version!

### Code Requirements
* Python >= 3.7
* PyQt5 >= 5.13
* Pillow >= 6.1 (used for image processing)

### Optional Requirements
* PyQt5-Tools >= 5.11.3 (if you plan to update the QT Designer .ui files)
* PyInstaller >= 3.5 (if you plan on bundling the package into one executable)

### Running (from source)
Clone this repository using git, then run *"gui/main\_mcb\_editor.py"*

## Mega Man X8 Level Editor
I am currently working on a level editor (for enemies only) as I am not well versed in 3D modeling to make a 3D editor.

It is not ready for testing, but if you want to try it then you can run it from *"gui/main\_set\_editor.py"*

## License
The MIT License (see LICENSE)

## Acknowledgments
* ARCtool by FluffyQuack (v0.9.428) which allowed for editing on X Legacy Collection 2 for PC