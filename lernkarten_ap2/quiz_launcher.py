"""
Quiz Launcher für AP2 Lernkarten
Ruft die C# Quiz-Anwendung aus der Python/PyQt6 GUI auf
"""

import subprocess
import os
from pathlib import Path

class AP2QuizLauncher:
    def __init__(self, executable_path: str = None):
        """
        Initialisiert den Quiz Launcher
        
        Args:
            executable_path: Pfad zur main.exe. Falls None, wird aktuelles Verzeichnis verwendet
        """
        if executable_path is None:
            self.exe_path = Path(__file__).parent / "main.exe"
        else:
            self.exe_path = Path(executable_path)
        
        self.working_dir = self.exe_path.parent

    def start_quiz(self) -> bool:
        """
        Startet die Quiz-Anwendung
        
        Returns:
            True wenn erfolgreich gestartet, False wenn Fehler
        """
        if not self.exe_path.exists():
            print(f"Fehler: Quiz-Exe nicht gefunden: {self.exe_path}")
            return False
        
        try:
            subprocess.Popen(
                [str(self.exe_path)],
                cwd=str(self.working_dir),
                shell=False
            )
            return True
        except Exception as e:
            print(f"Fehler beim Starten des Quiz: {e}")
            return False

    def initialize_counter(self) -> bool:
        """
        Initialisiert die Counter-JSON Datei
        
        Returns:
            True wenn erfolgreich, False wenn Fehler
        """
        if not self.exe_path.exists():
            print(f"Fehler: Quiz-Exe nicht gefunden: {self.exe_path}")
            return False
        
        try:
            result = subprocess.run(
                [str(self.exe_path), "--setup"],
                cwd=str(self.working_dir),
                capture_output=True,
                text=True
            )
            if result.returncode == 0:
                print(result.stdout)
                return True
            else:
                print(f"Fehler: {result.stderr}")
                return False
        except Exception as e:
            print(f"Fehler beim Initialisieren des Counter: {e}")
            return False


# Beispiel-Nutzung
if __name__ == "__main__":
    launcher = AP2QuizLauncher()
    
    # Beispiel: Quiz starten
    if launcher.start_quiz():
        print("Quiz gestartet!")
    else:
        print("Quiz konnte nicht gestartet werden")
