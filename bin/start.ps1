<#
.SYNOPSIS
  One command from the repo root. Starts the workshop relay and opens the
  landing page with the relay access token already attached.

.DESCRIPTION
  What it does, in order:
    1. runs bin\doctor.ps1 and stops if the relay path is not ready
    2. picks a Python interpreter that has aiohttp, creating .venv\ if needed
    3. mints a relay access token and pins it for this run
    4. opens index.html#relay_token=... in your browser
    5. runs ai-village-workshop\relay.py in the foreground

  Stop it with Ctrl+C. That stops the relay and nothing else.

  You do not need this script to run the workshop. Recorded playback works by
  opening index.html directly, with no relay and no Python at all.

  The relay hardcodes port 3001 and binds 127.0.0.1. There is no switch here
  to change either one, because there is no way to change them in relay.py.

.EXAMPLE
  bin\start.ps1
.EXAMPLE
  bin\start.ps1 -NoBrowser
.EXAMPLE
  bin\start.ps1 -SkipChecks -Model claude-sonnet-4-6
#>
[CmdletBinding()]
param(
  [switch]$NoBrowser,
  [switch]$SkipChecks,
  [string]$Model = ''
)

$ErrorActionPreference = 'Stop'
$root     = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
$workshop = Join-Path $root 'ai-village-workshop'
$relay    = Join-Path $workshop 'relay.py'

if (-not (Test-Path -LiteralPath $relay -PathType Leaf)) {
  Write-Error "start: cannot find $relay. Run this from the repo root, as bin\start.ps1"
  exit 1
}

# ------------------------------------------------------------- pre-flight
if (-not $SkipChecks) {
  & (Join-Path $root 'bin/doctor.ps1')
  $doctorRc = $LASTEXITCODE
  if ($doctorRc -ne 0) {
    Write-Host ""
    Write-Host "start: doctor reported problems (exit $doctorRc)." -ForegroundColor Red
    Write-Host "start: if the LIVE RELAY line said READY you can continue with -SkipChecks."
    exit 1
  }
}

# ------------------------------------------------------------- interpreter
$python = $null
$venvPy = Join-Path $root '.venv/Scripts/python.exe'

function Test-Aiohttp { param($exe) try { (& $exe -c 'import aiohttp;print(1)' 2>$null) -eq '1' } catch { $false } }

if ((Test-Path -LiteralPath $venvPy) -and (Test-Aiohttp $venvPy)) {
  $python = $venvPy
  Write-Host "start: using .venv\ ($(& $python --version 2>&1))"
} else {
  $sys = $null
  foreach ($cand in @('python', 'python3', 'py')) {
    if (Get-Command $cand -ErrorAction SilentlyContinue) { $sys = $cand; break }
  }
  if (-not $sys) {
    Write-Host "start: no python on PATH." -ForegroundColor Red
    Write-Host "start: recorded playback needs no Python. Open index.html instead."
    exit 1
  }
  if (Test-Aiohttp $sys) {
    $python = (Get-Command $sys).Source
    Write-Host "start: using system $sys ($(& $sys --version 2>&1)), aiohttp already present"
  } else {
    Write-Host "start: aiohttp not found, creating .venv\ and installing it"
    & $sys -m venv (Join-Path $root '.venv')
    if ($LASTEXITCODE -ne 0) { Write-Error "start: could not create a virtualenv"; exit 1 }
    & (Join-Path $root '.venv/Scripts/pip.exe') install --quiet --upgrade pip aiohttp
    if ($LASTEXITCODE -ne 0) { Write-Error "start: pip could not install aiohttp into .venv\"; exit 1 }
    $python = $venvPy
    Write-Host "start: .venv\ ready ($(& $python --version 2>&1))"
  }
}

# ------------------------------------------------------------- token
# relay.py mints its own token when RELAY_TOKEN is unset, but then this script
# would not know it and could not build the landing-page link. So we mint it
# here. relay.py refuses any RELAY_TOKEN shorter than 16 characters.
$token = (& $python -c 'import secrets;print(secrets.token_urlsafe(24))' 2>$null)
if (-not $token -or $token.Length -lt 16) {
  Write-Error "start: failed to mint a relay token"
  exit 1
}
$env:RELAY_TOKEN = $token
if ($Model) { $env:RELAY_MODEL = $Model }

$indexPath = Join-Path $root 'index.html'
$landing   = "file:///$($indexPath -replace '\\','/')#relay_token=$token"

Write-Host ""
Write-Host "  relay        http://localhost:3001  (127.0.0.1 only)"
Write-Host "  landing      file:///$($indexPath -replace '\\','/')"
Write-Host "  token        $token  (this run only)"
Write-Host "  stop         Ctrl+C"
Write-Host ""

# ------------------------------------------------------------- browser
if (-not $NoBrowser) {
  Start-Job -ScriptBlock {
    param($url) Start-Sleep -Milliseconds 1500; Start-Process $url
  } -ArgumentList $landing | Out-Null
}

# ------------------------------------------------------------- relay
Set-Location -LiteralPath $workshop
& $python 'relay.py'
exit $LASTEXITCODE
