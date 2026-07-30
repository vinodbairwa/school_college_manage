# EduNest one-command starter for Windows PowerShell
# Usage:  .\start-all.ps1
Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"
Set-Location -Path $PSScriptRoot

if (-not (Get-Command node -ErrorAction SilentlyContinue)) {
  Write-Error "Node.js not found. Install Node 20+ from https://nodejs.org"
}

if (-not (Get-Command python -ErrorAction SilentlyContinue) -and -not (Get-Command py -ErrorAction SilentlyContinue)) {
  Write-Error "Python not found. Install Python 3.12+ and enable 'Add to PATH'."
}

npm install
node scripts/start-all.mjs
