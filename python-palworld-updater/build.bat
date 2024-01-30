@echo off
pyinstaller -F -w -i resource\icon.ico --add-data="resource\icon.ico;resource" -n PalUpdater main.py
pause
