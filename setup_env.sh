#!/usr/bin/env bash
set -e

# Simple environment setup script for the Autonomous Web UI Testing Agent
# Usage (from repository root):
#   chmod +x setup_env.sh
#   ./setup_env.sh

PYTHON_BIN=${PYTHON_BIN:-python}

$PYTHON_BIN -m venv .venv

if [ -d ".venv/Scripts" ]; then
  # Windows-style virtual environment (Git Bash / MSYS)
  source .venv/Scripts/activate
else
  # POSIX-style virtual environment
  source .venv/bin/activate
fi

pip install --upgrade pip
pip install -r requirements.txt

# Install Playwright browsers (optional but recommended)
$PYTHON_BIN -m playwright install
