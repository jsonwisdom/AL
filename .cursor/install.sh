#!/usr/bin/env bash
# Idempotent Cloud Agent bootstrap for the AL / ALMS repository.
#
# Prepares both toolchains the repo's canonical flows depend on:
#   - Python: `python verify_all.py` -> CONSTITUTIONAL_REPLAY_PASS
#             `./reproduce.sh`        -> REPLAY_CONFIRMED
#   - Node:   witness emit/verify pipeline and `server.js`
#
# Safe to run repeatedly: every step converges to the same state.
set -euo pipefail

cd "$(dirname "$0")/.."

echo "==> Ensuring the 'python' command is available (repo scripts shell out to 'python')"
if ! command -v python >/dev/null 2>&1; then
  sudo apt-get update -qq
  sudo apt-get install -y python-is-python3
fi
python --version

echo "==> Installing Python dependencies (verifier + ledger tooling)"
# Non-root pip installs land in the user site; --break-system-packages keeps this
# working even when the base image marks the interpreter as externally managed.
python -m pip install --user --break-system-packages -r requirements.txt pytest

echo "==> Installing Node dependencies from lockfile"
npm ci

echo "==> Bootstrap complete"
