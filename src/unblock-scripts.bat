@echo off
echo Dosyalarin engeli kaldiriliyor...
powershell -command "dir .\*.ps1 | Unblock-File"
echo Islem tamamlandi.
pause > NUL