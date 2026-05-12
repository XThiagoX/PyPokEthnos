#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

if [[ "${1:-}" == "--headless" ]]; then
  HEADLESS=1
else
  HEADLESS=0
fi

if ! command -v python3 >/dev/null 2>&1; then
  echo "python3 nao encontrado. Instale Python 3."
  exit 1
fi

if ! python3 -c "import tkinter" >/dev/null 2>&1; then
  echo "Tkinter nao encontrado. Em Ubuntu, execute: sudo apt update && sudo apt install -y python3-tk"
  exit 1
fi

if [[ ! -d ".venv" ]]; then
  python3 -m venv .venv
fi

# shellcheck disable=SC1091
source .venv/bin/activate

pip install --upgrade pip
pip install -r requirements.txt

if [[ "$HEADLESS" -eq 1 ]]; then
  if ! command -v xvfb-run >/dev/null 2>&1; then
    echo "xvfb-run nao encontrado. Em Ubuntu, execute: sudo apt install -y xvfb"
    exit 1
  fi
  exec xvfb-run -a python src/main.py
fi

if [[ -z "${DISPLAY:-}" ]]; then
  echo "DISPLAY vazio. Use --headless no Codespaces/CI: ./scripts/setup_and_run_linux.sh --headless"
  exit 1
fi

exec python src/main.py
