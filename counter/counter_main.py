#---------------------------------------------------------------------------------------------------------------------------------------------
#importe <----------------------------<------------------------------<------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------------------------
import sys  # noqa: F401 – wird in __main__ benötigt
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (QApplication, QDialog, QPushButton, QVBoxLayout, 
                               QHBoxLayout, QLabel)

try:
    from utils.git_utils import git_pull as git_pull_db, git_push as git_push_db
    from counter.under_funktions import update_counter, get_counter_display_text
except ImportError:
    try:
        from under_funktions import update_counter, get_counter_display_text
        from utils.git_utils import git_pull as git_pull_db, git_push as git_push_db
    except ImportError:
        def git_pull_db(): pass
        def git_push_db(): pass
        def update_counter(art): pass
        def get_counter_display_text():
            return "Zählerstände konnten nicht geladen werden.\nTechnisch: 0 | Allgemein: 0 | Gesamt: 0"
class CounterDialog(QDialog):
    """
    Hauptfenster für den Störungszähler im einem Modus.
    Erlaubt das Zählen und stellt sicher, dass alle Änderungen gespeichert (gepusht) werden.
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Störungs Counter (Admin)")
        self.setGeometry(0, 0, 280, 200)
        self.setWindowFlag(Qt.WindowStaysOnTopHint)        
        self.init_ui() 
        self.init_data()
#--------------------------------------------------------
#----> Gui Elemente <------------------------------------
#--------------------------------------------------------
    def init_ui(self):
        main_layout = QVBoxLayout()
        
        # hheader-Label
        self.header_label = QLabel("Fehlercounter für die Schulung")
        self.header_label.setAlignment(Qt.AlignCenter)
        self.header_label.setStyleSheet("font-weight: bold; font-size: 11pt;")
        main_layout.addWidget(self.header_label)

        # Label für Counter
        self.total_label = QLabel("Gesamt: --")
        self.total_label.setAlignment(Qt.AlignCenter)
        self.total_label.setWordWrap(True)
        main_layout.addWidget(self.total_label)
        
        # Buttons sind immer sichtbar
        counter_button_layout = QHBoxLayout()
        self.tech_button = QPushButton("Technische Störung zählen")
        self.tech_button.clicked.connect(lambda: self.count_störung("technisch"))
        counter_button_layout.addWidget(self.tech_button)
        
        self.general_button = QPushButton("Allgemeine Störung zählen")
        # Korrigierter Tippfehler "algemein"
        self.general_button.clicked.connect(lambda: self.count_störung("algemein")) 
        counter_button_layout.addWidget(self.general_button)
        
        main_layout.addLayout(counter_button_layout)
        
        # Schließen-Button
        self.close_button = QPushButton("Schließen & Speichern")
        # Ruft direkt accept() auf, das den Push garantiert
        self.close_button.clicked.connect(self.accept) 
        main_layout.addWidget(self.close_button)

        self.setLayout(main_layout)
        self.update_display() # Erste Anzeige nach UI-Setup laden
        
    def init_data(self):
        """Initialisiert DB, zieht und pusht beim Start (Admin-Modus)."""
        git_pull_db()
        # Initialer Push (wie im Original-Tkinter-Admin-Modus)
        git_push_db() 

    def count_störung(self, art):
        """Erhöht den Zähler, aktualisiert die Anzeige und pusht sofort."""
        update_counter(art)
        self.update_display()
        git_push_db()

    def update_display(self):
        """Aktualisiert die Labels mit dem formatierten Text aus der Helferfunktion."""
        try:
            display_text = get_counter_display_text()
            self.total_label.setText(display_text)
        except Exception:
            self.total_label.setText("Fehler beim Laden der Zählerstände.")

    def reject(self):
        """Wird bei Schließen über X/ESC aufgerufen."""
        git_push_db()
        super().reject()

    def accept(self):
        """Wird bei Klick auf 'Schließen & Speichern' aufgerufen."""
        git_push_db()
        super().accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    dialog = CounterDialog()
    dialog.exec()
    sys.exit(app.exec())