import sys
import os
import json
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QDialog, QLabel, QRadioButton, QCheckBox,
    QButtonGroup, QLineEdit, QHBoxLayout, QMessageBox, QComboBox
)
from PySide6.QtCore import Qt

DB_PATH = "quiz_app.sqlite"
SCORES_PATH = os.path.join(os.path.dirname(__file__), "quiz_scores.json")

# Hilfsfunktionen für Score-Handling

def lade_scores():
    if not os.path.exists(SCORES_PATH):
        return {}
    with open(SCORES_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def speichere_scores(scores):
    with open(SCORES_PATH, "w", encoding="utf-8") as f:
        json.dump(scores, f, indent=2)

# Hilfsfunktion: Hole Frage mit höchstem Fehler-Count
import sqlite3
def frage_mit_hoechstem_count():
    scores = lade_scores()
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT id, frage_text FROM frage")
    fragen = c.fetchall()
    conn.close()
    # Finde Frage mit höchstem Fehler-Count
    max_count = -9999
    beste_frage = None
    for frage_id, frage_text in fragen:
        count = scores.get(str(frage_id), 0)
        if count > max_count:
            max_count = count
            beste_frage = (frage_id, frage_text)
    return beste_frage

# Hauptmenü
class QuizMainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Quiz Menü")
        layout = QVBoxLayout(self)
        self.btn_frage_beantworten = QPushButton("Frage beantworten")
        self.btn_frage_hinzufuegen = QPushButton("Frage hinzufügen")
        layout.addWidget(self.btn_frage_beantworten)
        layout.addWidget(self.btn_frage_hinzufuegen)
        self.btn_frage_beantworten.clicked.connect(self.frage_beantworten)
        self.btn_frage_hinzufuegen.clicked.connect(self.frage_hinzufuegen)

    def frage_beantworten(self):
        frage = frage_mit_hoechstem_count()
        if not frage:
            QMessageBox.information(self, "Info", "Keine Fragen vorhanden.")
            return
        dialog = FrageBeantwortenDialog(frage[0], frage[1], self)
        dialog.exec()

    def frage_hinzufuegen(self):
        dialog = FrageHinzufuegenDialog(self)
        dialog.exec()

# Popup zum Beantworten einer Frage
class FrageBeantwortenDialog(QDialog):
    def __init__(self, frage_id, frage_text, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Frage beantworten")
        self.frage_id = frage_id
        self.frage_text = frage_text
        self.richtig_ids = set()
        self.antwort_checkboxes = []
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel(frage_text))
        # Antworten aus DB holen
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("SELECT id, antwort_text, ist_richtig FROM antwort WHERE frage_id = ?", (frage_id,))
        antworten = c.fetchall()
        conn.close()
        for antwort_id, antwort_text, ist_richtig in antworten:
            cb = QCheckBox(antwort_text)
            cb.setProperty("antwort_id", antwort_id)
            layout.addWidget(cb)
            self.antwort_checkboxes.append(cb)
            if ist_richtig:
                self.richtig_ids.add(antwort_id)
        # Buttons
        btn_layout = QHBoxLayout()
        self.btn_beenden = QPushButton("Beenden")
        self.btn_bearbeiten = QPushButton("Frage bearbeiten")
        self.btn_weiter = QPushButton("Weiter zur nächsten Frage")
        btn_layout.addWidget(self.btn_beenden)
        btn_layout.addWidget(self.btn_bearbeiten)
        btn_layout.addWidget(self.btn_weiter)
        layout.addLayout(btn_layout)
        self.btn_beenden.clicked.connect(self.accept)
        self.btn_bearbeiten.clicked.connect(self.frage_bearbeiten)
        self.btn_weiter.clicked.connect(self.antworten_auswerten)
        self.auswertung_gemacht = False

    def antworten_auswerten(self):
        if self.auswertung_gemacht:
            # Nächste Frage laden
            self.accept()
            parent = self.parent()
            if parent:
                parent.frage_beantworten()
            return
        gewaehlte = set(cb.property("antwort_id") for cb in self.antwort_checkboxes if cb.isChecked())
        scores = lade_scores()
        frage_id_str = str(self.frage_id)
        # Richtig: alle richtigen und nur richtige gewählt
        if gewaehlte == self.richtig_ids:
            QMessageBox.information(self, "Richtig!", "Super! Alle richtigen Antworten gewählt.")
            scores[frage_id_str] = scores.get(frage_id_str, 0) - 1
        else:
            QMessageBox.warning(self, "Falsch!", f"Falsch beantwortet! Richtige Antwort(en):\n" + self.richtige_antworten_text())
            scores[frage_id_str] = scores.get(frage_id_str, 0) + 1
        speichere_scores(scores)
        self.auswertung_gemacht = True
        self.btn_weiter.setText("Weiter zur nächsten Frage")

    def richtige_antworten_text(self):
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("SELECT antwort_text FROM antwort WHERE frage_id = ? AND ist_richtig = 1", (self.frage_id,))
        richtige = [row[0] for row in c.fetchall()]
        conn.close()
        return "\n".join(richtige)

    def frage_bearbeiten(self):
        dialog = FrageBearbeitenDialog(self.frage_id, self)
        dialog.exec()

# Dialog zum Bearbeiten einer Frage
class FrageBearbeitenDialog(QDialog):
    def __init__(self, frage_id, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Frage bearbeiten")
        self.frage_id = frage_id
        layout = QVBoxLayout(self)
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        frage_row = c.execute("SELECT frage_text FROM frage WHERE id = ?", (frage_id,)).fetchone()
        self.frage_input = QLineEdit(frage_row[0] if frage_row else "")
        layout.addWidget(QLabel("Fragetext:"))
        layout.addWidget(self.frage_input)
        self.antwort_inputs = []
        self.richtig_checks = []
        c.execute("SELECT id, antwort_text, ist_richtig FROM antwort WHERE frage_id = ?", (frage_id,))
        antworten = c.fetchall()
        for antwort_id, antwort_text, ist_richtig in antworten:
            h = QHBoxLayout()
            inp = QLineEdit(antwort_text)
            chk = QCheckBox("Richtig")
            chk.setChecked(bool(ist_richtig))
            h.addWidget(inp)
            h.addWidget(chk)
            layout.addLayout(h)
            self.antwort_inputs.append((antwort_id, inp))
            self.richtig_checks.append(chk)
        conn.close()
        btn_save = QPushButton("Speichern")
        layout.addWidget(btn_save)
        btn_save.clicked.connect(self.speichern)

    def speichern(self):
        frage_text = self.frage_input.text().strip()
        if not frage_text:
            QMessageBox.warning(self, "Fehler", "Fragetext darf nicht leer sein.")
            return
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("UPDATE frage SET frage_text = ? WHERE id = ?", (frage_text, self.frage_id))
        for (antwort_id, inp), chk in zip(self.antwort_inputs, self.richtig_checks):
            antwort_text = inp.text().strip()
            ist_richtig = 1 if chk.isChecked() else 0
            c.execute("UPDATE antwort SET antwort_text = ?, ist_richtig = ? WHERE id = ?", (antwort_text, ist_richtig, antwort_id))
        conn.commit()
        conn.close()
        QMessageBox.information(self, "Erfolg", "Frage aktualisiert.")
        self.accept()

# Dialog zum Hinzufügen einer neuen Frage
class FrageHinzufuegenDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Frage hinzufügen")
        layout = QVBoxLayout(self)
        self.frage_input = QLineEdit()
        layout.addWidget(QLabel("Fragetext:"))
        layout.addWidget(self.frage_input)
        self.antwort_inputs = []
        self.richtig_checks = []
        for i in range(4):
            h = QHBoxLayout()
            inp = QLineEdit()
            chk = QCheckBox("Richtig")
            h.addWidget(QLabel(f"Antwort {i+1}:"))
            h.addWidget(inp)
            h.addWidget(chk)
            layout.addLayout(h)
            self.antwort_inputs.append(inp)
            self.richtig_checks.append(chk)
        btn_save = QPushButton("Speichern")
        layout.addWidget(btn_save)
        btn_save.clicked.connect(self.speichern)

    def speichern(self):
        frage_text = self.frage_input.text().strip()
        antworten = [inp.text().strip() for inp in self.antwort_inputs if inp.text().strip()]
        richtig = [chk.isChecked() for chk in self.richtig_checks][:len(antworten)]
        if not frage_text or len(antworten) < 2:
            QMessageBox.warning(self, "Fehler", "Mindestens 2 Antworten und Fragetext erforderlich.")
            return
        if not any(richtig):
            QMessageBox.warning(self, "Fehler", "Mindestens eine Antwort muss als richtig markiert sein.")
            return
        if len(antworten) > 4:
            QMessageBox.warning(self, "Fehler", "Maximal 4 Antworten erlaubt.")
            return
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        # Neue ID generieren
        c.execute("SELECT MAX(id) FROM frage")
        max_id = c.fetchone()[0]
        neue_id = int(max_id)+1 if max_id else 1
        c.execute("INSERT INTO frage (id, frage_text, quiz_id) VALUES (?, ?, 1)", (neue_id, frage_text))
        for idx, antwort_text in enumerate(antworten):
            ist_richtig = 1 if richtig[idx] else 0
            c.execute("INSERT INTO antwort (antwort_text, frage_id, ist_richtig) VALUES (?, ?, ?)", (antwort_text, neue_id, ist_richtig))
        conn.commit()
        conn.close()
        QMessageBox.information(self, "Erfolg", "Frage hinzugefügt.")
        self.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = QuizMainWindow()
    window.show()
    sys.exit(app.exec())
