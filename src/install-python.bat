@echo off
cls
title OBA Otomatik Oynatici Python Installer

set isPythonInstalled = 
set /p "isPythonInstalled=[?] Is Python installed and in the path at your system? (Auto check:A, Yes:Y, No:N)"

if "%isPythonInstalled%"=="A" (
    python -V
    if errorlevel 1 (
        echo. & echo [!] Python isn't installed at your system.
        goto InstallPython
    ) 
    if errorlevel 0 (
        echo. & echo [i] Python is installed at your system.
        pause > NUL
        exit 0
    )
  
)
if "%isPythonInstalled%"=="N" (
    echo [!] Python isn't installed at your system.
    goto InstallPython
)
if "%isPythonInstalled%"=="Y" (
    echo [i] Python is installed at your system.
    pause > NUL
    exit 0
)

echo [!] Your answer isn't valid. (Auto check:A, Yes:Y, No:N)
pause > NUL
exit 1

:InstallPython

echo [i] Downloading Python installer...
if not exist "%TEMP%\python" mkdir "%TEMP%\python"

curl https://www.python.org/ftp/python/3.7.0/python-3.7.0.exe -o "%TEMP%\python\installer.exe"
if errorlevel 1 (
    echo. & echo [!] Requesting to Python server has failed. Check your internet connection or CURL may be not installed at your system.
    pause > NUL
    exit 1
)
echo [i] Python Installer downloaded.

title Python 3.7.0 Installer
echo [i] Starting Python Installer...
echo [!] Please be sure Python and PIP installed and added to PATH while you're installing Python with its installer.
"%TEMP%\python\installer.exe"
echo [i] Python Installer executed.

exit 0
