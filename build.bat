@echo off
pyinstaller -F -i resource\img\icon.ico --add-data="resource\img\icon.ico;resource" -n PalEditor main.py
set dir=dist\resource
if not exist %dir% mkdir %dir%
xcopy resource\* %dir% /E
pause
