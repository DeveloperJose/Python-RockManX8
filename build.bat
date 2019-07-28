@ECHO ON
CALL activate pyqt5

pyinstaller src/main.py ^
        --add-data resources/font.wpg;resources/font.wpg ^
        --add-data resources/mugshots.npz;resources/mugshots.npz ^
        --add-data resources/ARCtool.exe;resources/ARCtool.exe ^
        --upx-dir tools/upx-3.95-win64
        
@ECHO ON