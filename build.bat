@ECHO ON
CALL activate pyqt5

echo y | pyinstaller src/main_mcb_editor.py ^
        --add-data resources/default_font.wpg;resources ^
        --add-data resources/mugshots.pkl;resources ^
        --add-data resources/ARCtool.exe;resources
@ECHO ON