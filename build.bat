@echo off
pyinstaller --onefile -w -i resources\img\icon.ico --add-data="resources\img\icon.ico;resource" -n PalEditor main.py
set dir=dist\resources
if not exist %dir% mkdir %dir%
xcopy resources\* %dir% /E
pause
