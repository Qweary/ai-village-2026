#!/usr/bin/env bash
# bin/doctor.sh
#
# Pre-flight check for this conference package. Run it before you present.
#
# It reports two verdicts, because the package has two independent paths:
#
#   RECORDED PATH  Opening the slide decks and playing the recorded runs.
#                  Needs nothing but a browser and the files being present.
#                  This alone is enough to run the whole workshop.
#
#   LIVE RELAY     Driving the demos with real model calls through
#                  ai-village-workshop/relay.py. Needs Python and a provider.
#
# Exit status is 0 only when both paths are ready. A non-zero exit with
# "RECORDED PATH: READY" still means you can present.
#
# Usage:
#   bin/doctor.sh              full check
#   bin/doctor.sh --quiet      verdict lines only
#   bin/doctor.sh -h           this help

set -u

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
QUIET=0

while [ $# -gt 0 ]; do
  case "$1" in
    --quiet|-q) QUIET=1; shift;;
    -h|--help) sed -n '2,/^$/p' "$0" | sed 's/^#\{1,\} \{0,1\}//'; exit 0;;
    *) printf 'doctor: unknown flag: %s\n' "$1" >&2; exit 2;;
  esac
done

if [ -t 1 ] && command -v tput >/dev/null 2>&1 && [ -n "${TERM:-}" ]; then
  C_OK="$(tput setaf 2 2>/dev/null || true)"
  C_WARN="$(tput setaf 3 2>/dev/null || true)"
  C_BAD="$(tput setaf 1 2>/dev/null || true)"
  C_DIM="$(tput setaf 6 2>/dev/null || true)"
  C_OFF="$(tput sgr0 2>/dev/null || true)"
else
  C_OK=""; C_WARN=""; C_BAD=""; C_DIM=""; C_OFF=""
fi

# Verdict accumulators. 0 means still ready.
RECORDED_BAD=0
LIVE_BAD=0
WARN_COUNT=0

say()  { [ $QUIET -eq 1 ] || printf '%s\n' "$*"; }
ok()   { [ $QUIET -eq 1 ] || printf "  ${C_OK}PASS${C_OFF}  %s\n" "$1"; }
note() { [ $QUIET -eq 1 ] || printf "  ${C_DIM}INFO${C_OFF}  %s\n" "$1"; }
warn() { WARN_COUNT=$((WARN_COUNT + 1))
         [ $QUIET -eq 1 ] || printf "  ${C_WARN}WARN${C_OFF}  %s\n" "$1"
         [ $QUIET -eq 1 ] || [ $# -lt 2 ] || printf "        fix: %s\n" "$2"; }
bad()  { [ $QUIET -eq 1 ] || printf "  ${C_BAD}FAIL${C_OFF}  %s\n" "$1"
         [ $QUIET -eq 1 ] || [ $# -lt 2 ] || printf "        fix: %s\n" "$2"; }

say ""
say "${C_DIM}== Conference package doctor${C_OFF}"
say "   root: $ROOT"

# ---------------------------------------------------------------- package files
say ""
say "-- Package files"

# Files that must exist for the recorded path. A missing one here means the
# checkout is incomplete, not that the machine is short of something.
RECORDED_FILES="
index.html
ai-village-workshop/README.md
ai-village-workshop/ATTENDEE-SETUP.md
ai-village-workshop/WORKSHOP-GUIDE.md
ai-village-workshop/demos/swarm-factory-live.html
ai-village-workshop/demos/swarm-cage-live.html
ai-village-workshop/demos/improvement-loop-live.html
ai-village-workshop/labs/LAB-1-FACTORY.md
ai-village-workshop/labs/LAB-2-CAGE.md
ai-village-workshop/labs/LAB-3-LOOP.md
talk-2/compiles-differently-slides.html
"

MISSING=0
FOUND=0
for f in $RECORDED_FILES; do
  if [ -f "$ROOT/$f" ]; then
    FOUND=$((FOUND + 1))
  else
    MISSING=$((MISSING + 1))
    bad "missing $f" "re-clone the package, or run doctor from the repo root"
    RECORDED_BAD=1
  fi
done
if [ $MISSING -eq 0 ]; then
  ok "$FOUND of $((FOUND + MISSING)) core files present"
else
  note "$FOUND of $((FOUND + MISSING)) core files present, $MISSING missing"
fi

# Talk 1 is a directory of its own, and the deck lives one level down in
# talk-1/slides/. Look for any deck rather than a fixed filename so a rename
# inside talk-1/ does not turn this into a false alarm.
TALK1_DECK="$(find "$ROOT/talk-1" -maxdepth 2 -name '*.html' -type f 2>/dev/null | head -1)"
if [ -n "$TALK1_DECK" ]; then
  ok "talk 1 deck present: ${TALK1_DECK#"$ROOT/"}"
else
  bad "no slide deck found in talk-1/" "talk-1/ should contain the deck for 'Swarms That Fight and Fix Each Other in a Cage'"
  RECORDED_BAD=1
fi

if [ -f "$ROOT/talk-2/unbounded-split/split_demo.py" ]; then
  ok "talk 2 runnable demo present: talk-2/unbounded-split/split_demo.py"
else
  warn "talk-2/unbounded-split/split_demo.py missing" "the talk 2 deck still works; only the runnable side demo is gone"
fi

# ---------------------------------------------------------------- python
say ""
say "-- Live relay (Python)"

PY=""
if command -v python3 >/dev/null 2>&1; then
  PY="$(command -v python3)"
elif command -v python >/dev/null 2>&1; then
  PY="$(command -v python)"
fi

PY_OK=no
if [ -n "$PY" ]; then
  PY_VER="$("$PY" -c 'import sys;print("%d.%d.%d" % sys.version_info[:3])' 2>/dev/null || echo unknown)"
  PY_OK="$("$PY" -c 'import sys;print("yes" if sys.version_info>=(3,9) else "no")' 2>/dev/null || echo no)"
  if [ "$PY_OK" = yes ]; then
    ok "Python $PY_VER ($PY)"
  else
    bad "Python $PY_VER is too old, the relay needs 3.9 or later" "install Python 3.9+, or use the recorded path which needs no Python"
    LIVE_BAD=1
  fi
else
  bad "no python3 on PATH" "install Python 3.9+, or use the recorded path which needs no Python"
  LIVE_BAD=1
fi

# aiohttp is the relay's one non-stdlib dependency. Missing is a warning, not a
# failure, because bin/start.sh creates a virtualenv and installs it on first
# run. Failing here would block start.sh from doing the thing that fixes it.
if [ "$PY_OK" = yes ]; then
  AIO_VER="$("$PY" -c 'import aiohttp;print(aiohttp.__version__)' 2>/dev/null || true)"
  if [ -n "$AIO_VER" ]; then
    ok "aiohttp $AIO_VER importable from $PY"
  elif [ -x "$ROOT/.venv/bin/python3" ] && "$ROOT/.venv/bin/python3" -c 'import aiohttp' 2>/dev/null; then
    VENV_VER="$("$ROOT/.venv/bin/python3" -c 'import aiohttp;print(aiohttp.__version__)')"
    ok "aiohttp $VENV_VER in .venv/ (bin/start.sh will use that interpreter)"
  else
    warn "aiohttp not importable" "bin/start.sh installs it into .venv/ on first run, or: pip install aiohttp"
  fi
fi

# ---------------------------------------------------------------- port 3001
# relay.py hardcodes PORT = 3001 and binds 127.0.0.1. There is no flag or
# environment variable to move it, so a busy port really does block the relay.
if [ "$PY_OK" = yes ]; then
  PORT_STATE="$("$PY" - <<'PYEOF' 2>/dev/null || echo unknown
import socket
s = socket.socket()
try:
    s.bind(('127.0.0.1', 3001))
    print('free')
except OSError:
    print('busy')
finally:
    s.close()
PYEOF
)"
  case "$PORT_STATE" in
    free) ok "port 3001 free" ;;
    busy)
      if command -v curl >/dev/null 2>&1 && \
         curl -fsS --max-time 3 http://127.0.0.1:3001/health >/dev/null 2>&1; then
        note "port 3001 is already serving a healthy relay, stop it before starting a new one"
      else
        bad "port 3001 in use by something that is not the relay" "stop that process; the relay hardcodes port 3001 and cannot be moved"
        LIVE_BAD=1
      fi ;;
    *) warn "could not test port 3001" "check it by hand before you present" ;;
  esac
fi

# ---------------------------------------------------------------- providers
say ""
say "-- Live model providers (any one is enough)"

PROVIDERS=0

if command -v claude >/dev/null 2>&1; then
  CLAUDE_VER="$(claude --version 2>/dev/null | head -1)"
  [ -n "$CLAUDE_VER" ] || CLAUDE_VER="version unknown"
  ok "claude CLI: $CLAUDE_VER ($(command -v claude))"
  PROVIDERS=$((PROVIDERS + 1))
else
  note "claude CLI not on PATH, so the relay path is unavailable"
fi

if command -v ollama >/dev/null 2>&1; then
  if command -v curl >/dev/null 2>&1 && \
     curl -fsS --max-time 3 http://127.0.0.1:11434/api/tags >/dev/null 2>&1; then
    MODELS="$(ollama list 2>/dev/null | tail -n +2 | grep -c . || true)"
    [ -n "$MODELS" ] || MODELS=0
    ok "ollama installed and serving, $MODELS model(s) pulled"
    if [ "$MODELS" -eq 0 ]; then
      warn "ollama has no models pulled" "ollama pull llama3.2"
    else
      PROVIDERS=$((PROVIDERS + 1))
    fi
  else
    note "ollama installed but not serving on 127.0.0.1:11434 (start it with: ollama serve)"
  fi
else
  note "ollama not installed, see ai-village-workshop/OLLAMA-SETUP.md"
fi

if [ $PROVIDERS -eq 0 ]; then
  warn "no live provider is usable on this machine" "recorded playback still runs every lab; see ai-village-workshop/ATTENDEE-SETUP.md"
fi

# ---------------------------------------------------------------- browser
say ""
say "-- Browser"

if command -v xdg-open >/dev/null 2>&1; then
  ok "xdg-open present, bin/start.sh can open the landing page for you"
elif command -v open >/dev/null 2>&1; then
  ok "open present, bin/start.sh can open the landing page for you"
else
  warn "no xdg-open or open on PATH" "open index.html in a browser by hand"
fi

# ---------------------------------------------------------------- verdict
say ""
if [ $RECORDED_BAD -eq 0 ]; then
  printf "  RECORDED PATH: ${C_OK}READY${C_OFF}   open index.html and present\n"
else
  printf "  RECORDED PATH: ${C_BAD}NOT READY${C_OFF}   files are missing, see FAIL lines above\n"
fi
if [ $LIVE_BAD -eq 0 ]; then
  printf "  LIVE RELAY:    ${C_OK}READY${C_OFF}   run bin/start.sh\n"
else
  printf "  LIVE RELAY:    ${C_BAD}NOT READY${C_OFF}   see FAIL lines above\n"
fi
printf "  warnings: %d\n" "$WARN_COUNT"

EXIT=0
[ $RECORDED_BAD -eq 0 ] && [ $LIVE_BAD -eq 0 ] || EXIT=1
say ""
exit $EXIT
