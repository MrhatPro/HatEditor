@echo off

REM Install required Python modules
pip install tkinter
pip install pygments

REM Delete this batch script
del "%~f0"
