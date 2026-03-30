#!/usr/bin/env python3
"""
Netzplan Übungs-GUI
Startet die GUI für zufällige Netzplan-Übungsaufgaben
"""

import sys
from pathlib import Path

# Stelle sicher, dass die Module im gleichen Verzeichnis gefunden werden
sys.path.insert(0, str(Path(__file__).parent))

from verwaltungstool.critical_path_analysis.critical_path_analysis_exercises import main

if __name__ == "__main__":
    main()
