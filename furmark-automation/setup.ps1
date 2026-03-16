# Script settings
param(
    [string]$PythonScript = ".\benchmark_Install_Script.py"
)

# Check if running as administrator
$IsAdmin = ([Security.Principal.WindowsPrincipal] `
    [Security.Principal.WindowsIdentity]::GetCurrent()
).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)

if (-not $IsAdmin) {
    Write-Host "Please run this script as an Administrator." -ForegroundColor Red
    exit 
}
# Always run from the folder this script lives in
Set-Location -Path $PSScriptRoot
# Check if Python is installed by trying 'python' then falling back to 'py'
$pythonExe = "python"
$pythonCheck = & $pythonExe --version 2>&1
$PythonInstalled = $LASTEXITCODE -eq 0

if (-not $PythonInstalled) {
    $pythonExe = "py"
    $pythonCheck = & $pythonExe --version 2>&1
    $PythonInstalled = $LASTEXITCODE -eq 0
}

if ($PythonInstalled) {
    Write-Host "Python is installed: $pythonCheck" -ForegroundColor Green
} else {
    Write-Host "Python not found. Downloading Python ..." -ForegroundColor Yellow

    $pythonUrl = "https://www.python.org/ftp/python/3.12.0/python-3.12.0-amd64.exe"
    $installerPath = "$env:TEMP\python-3.12.0-amd64.exe"

    Invoke-WebRequest -Uri $pythonUrl -OutFile $installerPath

    Write-Host "Installing Python ..." -ForegroundColor Yellow
    Start-Process -FilePath $installerPath -ArgumentList "/quiet InstallAllUsers=1 PrependPath=1" -Wait
    Write-Host "Python installation completed." -ForegroundColor Green

    # After installing, Windows updated the PATH on disk — but this PowerShell session
    # still has the OLD PATH loaded in memory. This line re-reads it from the registry
    # so that 'python' and 'pip' commands work without needing to open a new terminal.
    $env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + `
                [System.Environment]::GetEnvironmentVariable("Path","User")
}

# Ensure pip is installed and up to date.
# '$pythonExe -m pip' is safer than calling 'pip' directly — it uses whichever pip belongs
# to the Python install we just verified/installed, avoiding version mismatch issues.
Write-Host "Ensuring pip is up to date ..." -ForegroundColor Yellow
& $pythonExe -m ensurepip --upgrade   # installs pip if missing
& $pythonExe -m pip install --upgrade pip --quiet

# Install the requests module.
# '--quiet' suppresses the wall of text pip normally prints.
Write-Host "Installing required Python packages ..." -ForegroundColor Yellow
& $pythonExe -m pip install requests --quiet

Write-Host "All dependencies ready." -ForegroundColor Green

# Run Python Script
Write-Host "Running Python script: $PythonScript" -ForegroundColor Green
if (-not (Test-Path $PythonScript)) {
    Write-Host "Python script not found: $PythonScript" -ForegroundColor Red
    exit 1
}
& $pythonExe $PythonScript