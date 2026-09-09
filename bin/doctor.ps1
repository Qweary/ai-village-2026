<#
.SYNOPSIS
  Pre-flight check for this conference package. Run it before you present.

.DESCRIPTION
  Reports two verdicts, because the package has two independent paths:

    RECORDED PATH  Opening the slide decks and playing the recorded runs.
                   Needs nothing but a browser and the files being present.
                   This alone is enough to run the whole workshop.

    LIVE RELAY     Driving the demos with real model calls through
                   ai-village-workshop\relay.py. Needs Python and a provider.

  Exit code is 0 only when both paths are ready. A non-zero exit with
  "RECORDED PATH: READY" still means you can present.

.EXAMPLE
  bin\doctor.ps1
.EXAMPLE
  bin\doctor.ps1 -Quiet
#>
[CmdletBinding()]
param([switch]$Quiet)

$ErrorActionPreference = 'Continue'
$root = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)

$script:RecordedBad = 0
$script:LiveBad     = 0
$script:WarnCount   = 0

function Say  { param($m) if (-not $Quiet) { Write-Host $m } }
function Ok   { param($m) if (-not $Quiet) { Write-Host "  PASS  $m" -ForegroundColor Green } }
function Note { param($m) if (-not $Quiet) { Write-Host "  INFO  $m" -ForegroundColor Cyan } }
function Warn {
  param($m, $fix)
  $script:WarnCount++
  if (-not $Quiet) {
    Write-Host "  WARN  $m" -ForegroundColor Yellow
    if ($fix) { Write-Host "        fix: $fix" }
  }
}
function Bad {
  param($m, $fix)
  if (-not $Quiet) {
    Write-Host "  FAIL  $m" -ForegroundColor Red
    if ($fix) { Write-Host "        fix: $fix" }
  }
}

function Get-Cmd { param($n) (Get-Command $n -ErrorAction SilentlyContinue) }

Say ""
Say "== Conference package doctor"
Say "   root: $root"

# ------------------------------------------------------------- package files
Say ""
Say "-- Package files"

$recordedFiles = @(
  'index.html',
  'ai-village-workshop/README.md',
  'ai-village-workshop/ATTENDEE-SETUP.md',
  'ai-village-workshop/WORKSHOP-GUIDE.md',
  'ai-village-workshop/demos/swarm-factory-live.html',
  'ai-village-workshop/demos/swarm-cage-live.html',
  'ai-village-workshop/demos/improvement-loop-live.html',
  'ai-village-workshop/labs/LAB-1-FACTORY.md',
  'ai-village-workshop/labs/LAB-2-CAGE.md',
  'ai-village-workshop/labs/LAB-3-LOOP.md',
  'talk-2/compiles-differently-slides.html'
)

$found = 0; $missing = 0
foreach ($f in $recordedFiles) {
  if (Test-Path -LiteralPath (Join-Path $root $f) -PathType Leaf) {
    $found++
  } else {
    $missing++
    Bad "missing $f" "re-clone the package, or run doctor from the repo root"
    $script:RecordedBad = 1
  }
}
if ($missing -eq 0) { Ok "$found of $($found + $missing) core files present" }
else { Note "$found of $($found + $missing) core files present, $missing missing" }

# Talk 1 is a directory of its own. Look for a deck rather than a fixed
# filename so a rename inside talk-1\ does not turn this into a false alarm.
$talk1 = Get-ChildItem -LiteralPath (Join-Path $root 'talk-1') -Filter '*.html' -File -Recurse -Depth 1 -ErrorAction SilentlyContinue | Select-Object -First 1
if ($talk1) {
  Ok "talk 1 deck present: $($talk1.Name)"
} else {
  Bad "no slide deck found in talk-1\" "talk-1\ should contain the deck for 'Swarms That Fight and Fix Each Other in a Cage'"
  $script:RecordedBad = 1
}

if (Test-Path -LiteralPath (Join-Path $root 'talk-2/unbounded-split/split_demo.py') -PathType Leaf) {
  Ok "talk 2 runnable demo present: talk-2\unbounded-split\split_demo.py"
} else {
  Warn "talk-2\unbounded-split\split_demo.py missing" "the talk 2 deck still works; only the runnable side demo is gone"
}

# ------------------------------------------------------------- python
Say ""
Say "-- Live relay (Python)"

$py = $null
foreach ($cand in @('python3', 'python', 'py')) {
  if (Get-Cmd $cand) { $py = $cand; break }
}

$pyOk = $false
if ($py) {
  $pyVer = (& $py -c 'import sys;print("%d.%d.%d" % sys.version_info[:3])' 2>$null)
  $pyOk  = ((& $py -c 'import sys;print("yes" if sys.version_info>=(3,9) else "no")' 2>$null) -eq 'yes')
  if ($pyOk) {
    Ok "Python $pyVer ($((Get-Cmd $py).Source))"
  } else {
    Bad "Python $pyVer is too old, the relay needs 3.9 or later" "install Python 3.9+, or use the recorded path which needs no Python"
    $script:LiveBad = 1
  }
} else {
  Bad "no python on PATH" "install Python 3.9+, or use the recorded path which needs no Python"
  $script:LiveBad = 1
}

# aiohttp missing is a warning, not a failure: bin\start.ps1 creates a
# virtualenv and installs it on first run.
if ($pyOk) {
  $aio = (& $py -c 'import aiohttp;print(aiohttp.__version__)' 2>$null)
  $venvPy = Join-Path $root '.venv/Scripts/python.exe'
  if ($aio) {
    Ok "aiohttp $aio importable from $py"
  } elseif ((Test-Path -LiteralPath $venvPy) -and (& $venvPy -c 'import aiohttp;print(1)' 2>$null)) {
    $venvAio = (& $venvPy -c 'import aiohttp;print(aiohttp.__version__)' 2>$null)
    Ok "aiohttp $venvAio in .venv\ (bin\start.ps1 will use that interpreter)"
  } else {
    Warn "aiohttp not importable" "bin\start.ps1 installs it into .venv\ on first run, or: pip install aiohttp"
  }
}

# ------------------------------------------------------------- port 3001
# relay.py hardcodes PORT = 3001 and binds 127.0.0.1. There is no flag or
# environment variable to move it, so a busy port really does block the relay.
if ($pyOk) {
  $portState = (& $py -c "import socket
s=socket.socket()
try:
    s.bind(('127.0.0.1',3001)); print('free')
except OSError:
    print('busy')
finally:
    s.close()" 2>$null)
  if ($portState -eq 'free') {
    Ok "port 3001 free"
  } elseif ($portState -eq 'busy') {
    $healthy = $false
    try {
      $r = Invoke-WebRequest -Uri 'http://127.0.0.1:3001/health' -TimeoutSec 3 -UseBasicParsing -ErrorAction Stop
      if ($r.StatusCode -eq 200) { $healthy = $true }
    } catch { $healthy = $false }
    if ($healthy) {
      Note "port 3001 is already serving a healthy relay, stop it before starting a new one"
    } else {
      Bad "port 3001 in use by something that is not the relay" "stop that process; the relay hardcodes port 3001 and cannot be moved"
      $script:LiveBad = 1
    }
  } else {
    Warn "could not test port 3001" "check it by hand before you present"
  }
}

# ------------------------------------------------------------- providers
Say ""
Say "-- Live model providers (any one is enough)"

$providers = 0

if (Get-Cmd 'claude') {
  $cv = (& claude --version 2>$null | Select-Object -First 1)
  if (-not $cv) { $cv = 'version unknown' }
  Ok "claude CLI: $cv ($((Get-Cmd 'claude').Source))"
  $providers++
} else {
  Note "claude CLI not on PATH, so the relay path is unavailable"
}

if (Get-Cmd 'ollama') {
  $serving = $false
  try {
    $r = Invoke-WebRequest -Uri 'http://127.0.0.1:11434/api/tags' -TimeoutSec 3 -UseBasicParsing -ErrorAction Stop
    if ($r.StatusCode -eq 200) { $serving = $true }
  } catch { $serving = $false }
  if ($serving) {
    $models = @(& ollama list 2>$null | Select-Object -Skip 1 | Where-Object { $_.Trim() }).Count
    Ok "ollama installed and serving, $models model(s) pulled"
    if ($models -eq 0) { Warn "ollama has no models pulled" "ollama pull llama3.2" } else { $providers++ }
  } else {
    Note "ollama installed but not serving on 127.0.0.1:11434 (start it with: ollama serve)"
  }
} else {
  Note "ollama not installed, see ai-village-workshop\OLLAMA-SETUP.md"
}

if ($providers -eq 0) {
  Warn "no live provider is usable on this machine" "recorded playback still runs every lab; see ai-village-workshop\ATTENDEE-SETUP.md"
}

# ------------------------------------------------------------- verdict
Say ""
if ($script:RecordedBad -eq 0) {
  Write-Host "  RECORDED PATH: READY   open index.html and present" -ForegroundColor Green
} else {
  Write-Host "  RECORDED PATH: NOT READY   files are missing, see FAIL lines above" -ForegroundColor Red
}
if ($script:LiveBad -eq 0) {
  Write-Host "  LIVE RELAY:    READY   run bin\start.ps1" -ForegroundColor Green
} else {
  Write-Host "  LIVE RELAY:    NOT READY   see FAIL lines above" -ForegroundColor Red
}
Write-Host "  warnings: $($script:WarnCount)"
Say ""

if ($script:RecordedBad -eq 0 -and $script:LiveBad -eq 0) { exit 0 } else { exit 1 }
