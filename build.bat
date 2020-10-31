@ECHO OFF
CALL activate pyqt5

echo y | pyinstaller src/main.py ^
        --add-data resources/default_font.wpg;resources ^
        --add-data resources/mugshots.pkl;resources ^
        --add-data resources/ARCtool.exe;resources ^
        --add-data resources/icon.png;resources ^
        --icon resources/icon.ico ^
        --name "MegaManX8_Text_Editor" ^
        --onefile
        REM -w ^
PAUSE        
@ECHO ON