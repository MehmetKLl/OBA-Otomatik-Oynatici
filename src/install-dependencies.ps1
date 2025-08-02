$Host.UI.RawUI.WindowTitle = 'OBA Otomatik Oynatici Bagimlilik Yukleyicisi'

Add-Type -AssemblyName System.IO.Compression.FileSystem

$InitialWorkingDirectory = Get-Location
$PythonWorkingDirectory = "$Env:TEMP\OBA Otomatik Oynatici\app"

if ([System.IO.Directory]::Exists("$Env:TEMP\OBA Otomatik Oynatici")) {
    Read-Host "[i] Halihazirda kurulu ortam bulundu. Silinip yeni ortam kurulmasi icin herhangi Enter'a basin. (Cikis: CTRL+C)" | Out-Null

    Write-Host "[i] Dizin siliniyor..."
    try {
        Remove-Item -Path "$Env:TEMP\OBA Otomatik Oynatici" -Recurse -Force
    }
    catch {
         $_
         Write-Host "[!] Eski dizin silinirken bir hata olustu!" -ForegroundColor red -BackgroundColor black
         Write-Host "[!] `"$Env:TEMP\OBA Otomatik Oynatici`" dizinini ve alt dizinlerini kontrol edin ve dizinlerde bir uygulama acik olmadigindan emin olun." -ForegroundColor yellow
         Write-Host "[i] Cikiliyor..." 
         Start-Sleep 10
         exit 1
    }
}

Write-Host "[i] Dizin olusturuluyor..." 
New-Item -Path $Env:TEMP -Name "OBA Otomatik Oynatici" -ItemType Directory -Force 

Write-Host "[i] Python paketi indiriliyor..." 
try {
    Invoke-WebRequest -Uri http://www.python.org/ftp/python/3.7.0/python-3.7.0-embed-win32.zip -outFile "$Env:TEMP\OBA Otomatik Oynatici\python.zip" -TimeoutSec 15
}
catch {
    $_
    Write-Host "[!] Python paketi indirilirken bir hata olustu!" -ForegroundColor red -BackgroundColor black
    Write-Host "[!] Internet baglantisini, SSL sertifikalarini ya da `"$Env:TEMP\OBA Otomatik Oynatici\python.zip`" dosyasini kontrol edin." -ForegroundColor yellow
    Write-Host "[i] Cikiliyor..." 
    Start-Sleep 10
    exit 1
}
Write-Host "[i] Paket indirildi." 

Write-Host "[i] Paket cikariliyor..." 
try {
    [System.IO.Compression.ZipFile]::ExtractToDirectory("$Env:TEMP\OBA Otomatik Oynatici\python.zip", "$PythonWorkingDirectory")
}
catch {
    $_
    Write-Host "[!] Python paketi klasore cikarilirken bir hata olustu!" -ForegroundColor red -BackgroundColor black
    Write-Host "Cikiliyor..." 
    Start-Sleep 10
    exit 1
}
Write-Host "[i] Paket cikarildi.." 

Write-Host "[i] PIP paket yoneticisi indiriliyor..." 
try {
    Invoke-WebRequest -Uri https://bootstrap.pypa.io/pip/3.7/get-pip.py -outFile "$PythonWorkingDirectory\get-pip.py" -TimeoutSec 15
}
catch {
    $_
    Write-Host "[!] PIP indirilirken bir hata olustu!" -ForegroundColor red -BackgroundColor black
    Write-Host "[!] Internet baglantisini, SSL sertifikalarini ya da `"$PythonWorkingDirectory\get-pip.py`" dosyasini kontrol edin." -ForegroundColor yellow
    Write-Host "[i] Cikiliyor..." 
    Start-Sleep 10
    exit 1
}
Write-Host "[i] PIP indirildi." 

Set-Location -Path $PythonWorkingDirectory
[Environment]::CurrentDirectory = $PythonWorkingDirectory

Write-Host "[i] PIP kuruluyor..." 
$PIPInstallation = Start-Process -FilePath ".\python.exe" -ArgumentList "get-pip.py", "--no-warn-script-location" -NoNewWindow -Wait -PassThru
if ($PIPInstallation.ExitCode) {
    Write-Host "[!] PIP kurulurken bir hata olustu!" -ForegroundColor red -BackgroundColor black
    Write-Host "[i] Cikiliyor..." 
    Start-Sleep 10
    exit 1
}

$PTHFileContent = @"
python37.zip
.
$InitialWorkingDirectory\
.\Lib\site-packages\
import site
"@

[System.IO.File]::WriteAllLines(".\python37._pth", $PTHFileContent, (New-Object System.Text.UTF8Encoding $False))

Write-Host "[i] PIP kuruldu." 

Write-Host "[i] Kutuphaneler indiriliyor..." 
$LibraryInstallation = Start-Process -FilePath ".\python.exe" -ArgumentList "-m", "pip", "install", "-r", "$InitialWorkingDirectory\requirements.txt", "--isolated", "--no-warn-script-location", "--trusted-host=pypi.python.org", "--trusted-host=pypi.org", "--trusted-host=files.pythonhosted.org" -NoNewWindow -Wait -PassThru
if ($LibraryInstallation.ExitCode) {
    Write-Host "[!] Kutuphaneler kurulurken bir hata olustu!" -ForegroundColor red -BackgroundColor black
    Write-Host "[!] Internet baglantisini veya SSL sertifikalarini kontrol edin." -ForegroundColor yellow
    Write-Host "[i] Cikiliyor..." 
    Start-Sleep 10
    exit 1
}
Write-Host "[i] Kutuphaneler indirildi." 
Write-Host "[i] Tum bagimliliklar indirildi. Programin kaynak kodlarini run.ps1 ve main.ps1 dosyalari ile calistirabilirsiniz. Cikmak icin Enter'a basin." 
Read-Host | Out-Null
exit