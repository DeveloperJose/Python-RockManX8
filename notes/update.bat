@ECHO OFF

arctool -c -pc LABO_TIT
CALL activate py36
python update_arc.py
xcopy /Y /F "LABO_TIT.arc" "C:\Users\xeroj\Desktop\Programs\Steam\steamapps\common\Mega Man X Legacy Collection 2\nativeDX10\X8\romPC\data\mes\USA"

@ECHO ON