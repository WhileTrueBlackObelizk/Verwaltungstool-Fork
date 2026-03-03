#!/bin/bash
# Startet das Verwaltungstool und installiert PySide6 automatisch falls nötig

cd "$(dirname "$0")"

python3 -c "import PySide6" 2>/dev/null || {
    echo "PySide6 nicht gefunden – wird installiert..."
    python3 -m pip install -r requirements.txt
}

python3 main.py
