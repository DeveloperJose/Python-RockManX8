@ECHO OFF

xcopy /Y /F "USA ARCS\LABO_TIT.arc" ""
xcopy /Y /F "USA ARCS\CHIP_TIT.arc" ""
arctool -x -pc "LABO_TIT.arc"
arctool -x -pc "CHIP_TIT.arc"

REM arctool -x -pc -noextractdir "LABO_TIT.arc"

@ECHO ON