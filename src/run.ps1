$PythonWorkingDirectory = "$Env:TEMP\OBA Otomatik Oynatici\app"

if (!([System.IO.File]::Exists("$PythonWorkingDirectory\python.exe"))) {
    Write-Host "[!] Kodun yurutulmesi icin gerekli olan dosyalar yuklu degil! Ilk once install-dependencies.ps1 dosyasini indirin." -ForegroundColor yellow
    Start-Sleep 10
    exit 1
}

Write-Host "[i] Calistiriliyor..."
try {
    Start-Process -FilePath "$PythonWorkingDirectory\python.exe" -ArgumentList ".\run.py" -NoNewWindow -Wait
}
catch {
    Write-Host "[!] Kod yurutulurken bir hata olustu!" -ForegroundColor red -BackgroundColor black
    Start-Sleep 10
    exit 1
}