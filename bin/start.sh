#!/usr/bin/env bash
# bin/start.sh
#
# One command from the repo root. Starts the workshop relay and opens the
# landing page in your browser with the relay access token already attached,
# so the demos can make live calls without you copying anything.
#
# What it does, in order:
#   1. runs bin/doctor.sh and stops if the relay path is not ready
#   2. picks a Python interpreter that has aiohttp, creating .venv/ if needed
#   3. mints a relay access token and pins it for this run
#   4. opens index.html#relay_token=... in your browser
#   5. runs ai-village-workshop/relay.py in the foreground
#
# Stop it with Ctrl+C. That stops the relay and nothing else.
#
# You do not need this script to run the workshop. Recorded playback works by
# opening index.html directly, with no relay and no Python at all.
#
# Usage:
#   bin/start.sh                  normal start
#   bin/start.sh --no-browser     start the relay, open nothing
#   bin/start.sh --skip-checks    skip bin/doctor.sh
#   bin/start.sh --model NAME     override the relay model for this run
#   bin/start.sh -h               this help
#
# The relay hardcodes port 3001 and binds 127.0.0.1. There is no flag here to
# change either one, because there is no way to change them in relay.py.

set -u

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
WORKSHOP="$ROOT/ai-village-workshop"
OPEN_BROWSER=1
SKIP_CHECKS=0
MODEL=""

while [ $# -gt 0 ]; do
  case "$1" in
    --no-browser)  OPEN_BROWSER=0; shift;;
    --skip-checks) SKIP_CHECKS=1; shift;;
    --model)
      if [ $# -lt 2 ]; then printf 'start: --model needs a value\n' >&2; exit 2; fi
      MODEL="$2"; shift 2;;
    -h|--help) sed -n '2,/^$/p' "$0" | sed 's/^#\{1,\} \{0,1\}//'; exit 0;;
    *) printf 'start: unknown flag: %s\n' "$1" >&2; exit 2;;
  esac
done

if [ ! -f "$WORKSHOP/relay.py" ]; then
  printf 'start: cannot find %s\n' "$WORKSHOP/relay.py" >&2
  printf 'start: run this from the repo root, as bin/start.sh\n' >&2
  exit 1
fi

# --------------------------------------------------------------- pre-flight
if [ $SKIP_CHECKS -eq 0 ]; then
  if [ -x "$ROOT/bin/doctor.sh" ]; then
    "$ROOT/bin/doctor.sh"
    DOCTOR_RC=$?
  else
    bash "$ROOT/bin/doctor.sh"
    DOCTOR_RC=$?
  fi
  if [ $DOCTOR_RC -ne 0 ]; then
    printf '\nstart: doctor reported problems (exit %d).\n' "$DOCTOR_RC" >&2
    printf 'start: if the LIVE RELAY line said READY you can continue with --skip-checks.\n' >&2
    exit 1
  fi
fi

# --------------------------------------------------------------- interpreter
# Preference order: a .venv/ that already has aiohttp, then the system python3
# if it has aiohttp, then a fresh .venv/ we build here.
PYTHON=""

if [ -x "$ROOT/.venv/bin/python3" ] && "$ROOT/.venv/bin/python3" -c 'import aiohttp' 2>/dev/null; then
  PYTHON="$ROOT/.venv/bin/python3"
  printf 'start: using .venv/ (%s)\n' "$("$PYTHON" --version 2>&1)"
elif command -v python3 >/dev/null 2>&1 && python3 -c 'import aiohttp' 2>/dev/null; then
  PYTHON="$(command -v python3)"
  printf 'start: using system python3 (%s), aiohttp already present\n' "$(python3 --version 2>&1)"
elif command -v python3 >/dev/null 2>&1; then
  printf 'start: aiohttp not found, creating .venv/ and installing it\n'
  if ! python3 -m venv "$ROOT/.venv"; then
    printf 'start: could not create a virtualenv.\n' >&2
    printf 'start: on Debian and Kali try: sudo apt install python3-venv\n' >&2
    exit 1
  fi
  if ! "$ROOT/.venv/bin/pip" install --quiet --upgrade pip aiohttp; then
    printf 'start: pip could not install aiohttp into .venv/\n' >&2
    exit 1
  fi
  PYTHON="$ROOT/.venv/bin/python3"
  printf 'start: .venv/ ready (%s)\n' "$("$PYTHON" --version 2>&1)"
else
  printf 'start: no python3 on PATH.\n' >&2
  printf 'start: recorded playback needs no Python. Open index.html instead.\n' >&2
  exit 1
fi

# --------------------------------------------------------------- token
# relay.py mints its own token when RELAY_TOKEN is unset, but then this script
# would not know it and could not build the landing-page link. So we mint it
# here instead. relay.py refuses any RELAY_TOKEN shorter than 16 characters.
TOKEN="$("$PYTHON" -c 'import secrets;print(secrets.token_urlsafe(24))' 2>/dev/null)"
if [ -z "$TOKEN" ] || [ "${#TOKEN}" -lt 16 ]; then
  printf 'start: failed to mint a relay token (got %d characters)\n' "${#TOKEN}" >&2
  exit 1
fi
export RELAY_TOKEN="$TOKEN"
[ -n "$MODEL" ] && export RELAY_MODEL="$MODEL"

LANDING="file://$ROOT/index.html#relay_token=$TOKEN"

printf '\n'
printf '  relay        http://localhost:3001  (127.0.0.1 only)\n'
printf '  landing      %s\n' "file://$ROOT/index.html"
printf '  token        %s  (this run only)\n' "$TOKEN"
printf '  stop         Ctrl+C\n'
printf '\n'

# --------------------------------------------------------------- browser
if [ $OPEN_BROWSER -eq 1 ]; then
  if command -v xdg-open >/dev/null 2>&1; then
    ( sleep 1.5; xdg-open "$LANDING" >/dev/null 2>&1 ) &
  elif command -v open >/dev/null 2>&1; then
    ( sleep 1.5; open "$LANDING" >/dev/null 2>&1 ) &
  else
    printf 'start: no browser opener found. Open this URL by hand:\n'
    printf '  %s\n\n' "$LANDING"
  fi
fi

# --------------------------------------------------------------- relay
# exec so Ctrl+C reaches relay.py directly and this script leaves no wrapper
# process behind.
cd "$WORKSHOP" || exit 1
exec "$PYTHON" relay.py
