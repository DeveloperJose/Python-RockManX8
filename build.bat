@ECHO ON
CALL activate pyqt5

echo y | pyinstaller src/main_mcb_editor.py ^
        --add-data resources/default_font.wpg;resources ^
        --add-data resources/mugshots.pkl;resources ^
        --add-data resources/ARCtool.exe;resources ^
        --add-data resources/icon.png;resources ^
        --name "MegaManX8_Text_Editor" ^
        --icon resources/icon.ico ^
        --onefile
        REM -w ^
        
@ECHO ON