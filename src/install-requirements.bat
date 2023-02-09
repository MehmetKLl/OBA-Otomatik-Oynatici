@echo off
cls
title OBA Otomatik Oynatici Requirements Installer

python -V
if errorlevel 1 (
    echo. & echo [!] Python isn't installed or added to PATH.
    pause > NUL
    exit 1
)
if errorlevel 0 (
    echo. & echo [i] Python is installed at the system.
)

pip -V
if errorlevel 1 (
    echo. & echo [!] PIP isn't installed or added to PATH.
    pause > NUL
    exit 1
)  
if errorlevel 0 (
    echo. & echo [i] PIP is installed at the system.
)

pip install -r requirements.txt

if errorlevel 1 (
   echo. & echo [!] An unexpected error occured while downloading libraries.
   echo [!] Operation unsuccessful.
   pause > NUL
   exit 1
)
if errorlevel 0 (
    echo. & echo [i] Required libraries installed.
    pause > NUL
    exit 0
)