"""
Integration der AP2 Lernkarten Quiz in die Haupt-GUI (PyQt6 Beispiel)
Platziere diesen Code in deiner main.py oder in einem separaten Dialog
"""

from PySide6.QtWidgets import QPushButton, QDialog, QVBoxLayout, QLabel, QMessageBox
from PySide6.QtCore import Qt
import sys
from pathlib import Path

# Import der Quiz-Launcher Klasse
sys.path.insert(0, str(Path(__file__).parent / "lernkarten_ap2"))
from quiz_launcher import AP2QuizLauncher


class AP2QuizDialog(QDialog):
    """Dialog zum Starten des AP2 Lernkarten Quiz"""
    
    def __init__(self, parent=None, quiz_exe_path: str = None):
        super().__init__(parent)
        self.setWindowTitle("AP2 Lernkarten Quiz")
        self.setGeometry(100, 100, 400, 200)
        self.launcher = AP2QuizLauncher(quiz_exe_path)
        self.init_ui()
    
    def init_ui(self):
        """Initialisiert die UI"""
        layout = QVBoxLayout()
        
        # Infotekt
        info_label = QLabel(
            "AP2 Lernkarten Quiz\n\n"
            "Starte das Quiz, um dein Wissen zu testen.\n"
            "Die Fragen werden nach Schwierigkeit ausgewählt."
        )
        info_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(info_label)
        
        # Start-Button
        start_btn = QPushButton("Quiz Starten")
        start_btn.clicked.connect(self.on_start_quiz)
        layout.addWidget(start_btn)
        
        # Initialize-Button (Optional - nur für erste Einrichtung)
        init_btn = QPushButton("Counter initialisieren (nur beim ersten Mal)")
        init_btn.clicked.connect(self.on_initialize)
        layout.addWidget(init_btn)
        
        self.setLayout(layout)
    
    def on_start_quiz(self):
        """Startet das Quiz"""
        if self.launcher.start_quiz():
            QMessageBox.information(self, "Erfolg", "Quiz wurde gestartet!")
            self.accept()
        else:
            QMessageBox.critical(self, "Fehler", "Quiz konnte nicht gestartet werden!")
    
    def on_initialize(self):
        """Initialisiert die Counter-Datei"""
        if self.launcher.initialize_counter():
            QMessageBox.information(
                self, 
                "Erfolg", 
                "Counter wurde initialisiert!\n"
                "Das Quiz ist jetzt einsatzbereit."
            )
        else:
            QMessageBox.critical(self, "Fehler", "Initialisierung fehlgeschlagen!")


# ===== BEISPIEL-INTEGRATION IN HAUPT-GUI =====
# Füge das in deine main.py ein:

"""
# In deiner Main-Window Klasse:

def on_ap2_quiz_clicked(self):
    # Path zur quiz.exe relativ zur Haupt-GUI berechnen
    quiz_exe = Path(__file__).parent / "lernkarten_ap2" / "main.exe"
    
    dialog = AP2QuizDialog(self, str(quiz_exe))
    dialog.exec()

# Im init_ui():
ap2_button = QPushButton("AP2 Lernkarten Quiz")
ap2_button.clicked.connect(self.on_ap2_quiz_clicked)
main_layout.addWidget(ap2_button)
"""
