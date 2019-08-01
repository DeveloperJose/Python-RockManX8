@ECHO ON
CALL activate pyqt5

echo y | pyinstaller src/main.py ^
        --add-data resources/font.wpg;resources/font.wpg ^
        --add-data resources/mugshots.npz;resources/mugshots.npz ^
        --add-data resources/ARCtool.exe;resources/ARCtool.exe ^
        --hidden-import "sentry_sdk.integrations.logging" ^
        --hidden-import "sentry_sdk.integrations.stdlib" ^
        --hidden-import "sentry_sdk.integrations.excepthook" ^ 
        --hidden-import "sentry_sdk.integrations.dedupe"
        REM --log-level=DEBUG ^
        REM --upx-dir tools/upx-3.95-win64        
@ECHO ON