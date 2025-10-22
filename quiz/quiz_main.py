"""
Schüler-Quiz-GUI:
- Auswahl des eigenen Namens (inkl. Surren und Florian)
- Quiz-Auswahl und Sortierung
- Quiz starten
"""

import os
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QComboBox, QListWidget, QMessageBox, QHBoxLayout, QDialog, QRadioButton, QButtonGroup, QScrollArea, QLineEdit
from utils.git_utils import git_push
from quiz.quiz_score_manager import aktualisiere_frage
import sqlite3
import sys        

DB_PATH = "quiz_app.sqlite"

REPO_PATH = "."


class QuizDialog(QDialog):
    def __init__(self, schueler_name, quiz_id, quiz_titel):
        super().__init__()
        # Fenster-Titel setzen
        self.setWindowTitle(f"Quiz: {quiz_titel}")
        self.schueler_name = schueler_name  # Name des aktuellen Schülers
        self.quiz_id = quiz_id              # ID des aktuellen Quiz
        self.fragen = []                    # Liste der Fragen (frage_id, ButtonGroup)
        self.antwortgruppen = []            # Liste der ButtonGroups für Antworten

        # ScrollArea für viele Fragen, damit alles sichtbar bleibt
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        main_widget = QWidget()
        self.layout = QVBoxLayout(main_widget)  # Layout für Fragen und Antworten
        scroll.setWidget(main_widget)
        dialog_layout = QVBoxLayout(self)
        dialog_layout.addWidget(scroll)
        self.setLayout(dialog_layout)

        # Fragen und Antworten aus der Datenbank laden
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("SELECT id, frage_text FROM frage WHERE quiz_id = ?", (quiz_id,))
        fragen = c.fetchall()
        if not fragen:
            self.layout.addWidget(QLabel("Keine Fragen im Quiz vorhanden."))
        # Jede Frage einzeln abarbeiten
        for frage_id, frage_text in fragen:
            self.layout.addWidget(QLabel(frage_text)) # Frage anzeigen
            c.execute("SELECT id, antwort_text FROM antwort WHERE frage_id = ?", (frage_id,))
            antworten = c.fetchall()
            group = QButtonGroup(self) # ButtonGroup für Antwortoptionen
            # Jede Antwort als Radiobutton anzeigen
            for antwort_id, antwort_text in antworten:
                radio = QRadioButton(antwort_text) # Antwortoption als Radiobutton
                radio.setProperty("antwort_id", antwort_id) # Antwort-ID speichern
                group.addButton(radio)
                self.layout.addWidget(radio)
            self.fragen.append((frage_id, group)) # Frage und zugehörige Antworten speichern
            self.antwortgruppen.append(group)
        conn.close()

        # Button zum Abschicken der Antworten
        self.submit_btn = QPushButton("Abschicken")
        self.submit_btn.clicked.connect(self.submit_quiz)
        self.layout.addWidget(self.submit_btn)

    def submit_quiz(self):
        if not self.fragen:
            QMessageBox.information(self, "Info", "Es sind keine Fragen im Quiz vorhanden.")
            self.accept()
            return
        # Prüfen ob alle Fragen beantwortet wurden
        gegeben_antworten = [] # Liste der gewählten Antworten
        for frage_id, group in self.fragen:
            checked = group.checkedButton()
            if checked is None:
                # Wenn eine Frage nicht beantwortet wurde, abbrechen
                QMessageBox.warning(self, "Fehler", "Bitte alle Fragen beantworten!")
                return
            antwort_id = checked.property("antwort_id")
            gegeben_antworten.append((frage_id, antwort_id))
        # Ergebnis berechnen und speichern
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        # Schüler-ID aus Datenbank holen
        schueler_id = c.execute("SELECT id FROM schueler WHERE name = ?", (self.schueler_name,)).fetchone()[0]
        richtig = 0 # Zähler für richtige Antworten
        falsch = 0  # Zähler für falsche Antworten
        # Für jede Antwort prüfen ob sie richtig ist
        for frage_id, antwort_id in gegeben_antworten:
            ist_richtig = c.execute("SELECT ist_richtig FROM antwort WHERE id = ?", (antwort_id,)).fetchone()[0]
            aktualisiere_frage(self.schueler_name, frage_id, ist_richtig)
            if ist_richtig:
                richtig += 1
            else:
                falsch += 1
        # Aktuelles Datum/Uhrzeit für das Ergebnis
        import datetime
        datum = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # Ergebnis in die Datenbank schreiben
        c.execute("INSERT INTO ergebnis (schueler_id, quiz_id, datum, richtig, falsch) VALUES (?, ?, ?, ?, ?)",
                  (schueler_id, self.quiz_id, datum, richtig, falsch))
        ergebnis_id = c.lastrowid
        # Gegebene Antworten speichern
        for frage_id, antwort_id in gegeben_antworten:
            c.execute("INSERT INTO gegebene_antwort (ergebnis_id, frage_id, antwort_id) VALUES (?, ?, ?)",
                      (ergebnis_id, frage_id, antwort_id))
        conn.commit()
        conn.close()
        # Ergebnis zu Git pushen, damit Lehrer es sehen kann
        git_push(REPO_PATH)
        # Ergebnis dem Schüler einmalig anzeigen
        QMessageBox.information(self, "Ergebnis", f"Richtig: {richtig}\nFalsch: {falsch}")
        self.accept() # Dialog schließen

# Haupt-GUI für Schüler
class SchuelerQuizApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Quiz für Schüler")
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        # Dropdown für Schülernamen
        self.schueler_dropdown = QComboBox()
        self.layout.addWidget(QLabel("Wähle deinen Namen:"))
        self.layout.addWidget(self.schueler_dropdown)
        # Filter für Quiz-Sortierung
        filter_layout = QHBoxLayout()
        self.quiz_sort_dropdown = QComboBox()
        self.quiz_sort_dropdown.addItems([
            "Standard",         # Standard-Sortierung
            "Wie oft gemacht",  # Nach Häufigkeit
            "Wann erstellt",    # Nach Erstellungsdatum
            "Noch nie gemacht"  # Noch nicht bearbeitete Quiz
        ]) 
        #TODO: Fehlerhäufigkeiten (falsch - noch nicht richtig - richtig - perfekt)
        filter_layout.addWidget(QLabel("Quiz sortieren nach:"))
        filter_layout.addWidget(self.quiz_sort_dropdown)
        self.layout.addLayout(filter_layout)
        # Liste der verfügbaren Quiz
        self.quiz_list = QListWidget()
        self.layout.addWidget(QLabel("Verfügbare Quiz:"))
        self.layout.addWidget(self.quiz_list)
        # Button zum Starten des Quiz
        self.start_button = QPushButton("Quiz starten")
        self.layout.addWidget(self.start_button)
        # Event-Handler verbinden
        self.start_button.clicked.connect(self.start_quiz)
        self.quiz_sort_dropdown.currentIndexChanged.connect(self.load_quiz)
        self.schueler_dropdown.currentIndexChanged.connect(self.load_quiz)
        # Initiales Laden der Schüler und Quiz
        self.load_schueler()
        self.load_quiz()

    def load_schueler(self):
        # Schülernamen aus DB laden, ggf. "Surren" und "Florian" hinzufügen
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        for name in ["Surren", "Florian"]:
            c.execute("SELECT id FROM schueler WHERE name = ?", (name,))
            if not c.fetchone():
                c.execute("INSERT INTO schueler (name) VALUES (?)", (name,))
        conn.commit()
        c.execute("SELECT name FROM schueler")
        schueler = c.fetchall()
        self.schueler_dropdown.clear()
        for s in schueler:
            self.schueler_dropdown.addItem(s[0])
        conn.close()

    def load_quiz(self):
        # Quizliste nach Sortiermodus laden
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        schueler = self.schueler_dropdown.currentText()
        sort_mode = self.quiz_sort_dropdown.currentText()
        # Verschiedene Sortiermodi für Quiz-Auswahl
        query = "SELECT quiz.id, quiz.titel, quiz.rowid, quiz.id FROM quiz"
        if sort_mode == "Wie oft gemacht" and schueler:
            # Quiz nach Häufigkeit sortieren
            query = """
                SELECT quiz.id, quiz.titel, COUNT(ergebnis.id) as gemacht_count
                FROM quiz
                LEFT JOIN ergebnis ON quiz.id = ergebnis.quiz_id AND ergebnis.schueler_id = (SELECT id FROM schueler WHERE name = ?)
                GROUP BY quiz.id
                ORDER BY gemacht_count DESC
            """
            c.execute(query, (schueler,))
            quiz = c.fetchall()
        elif sort_mode == "Wann erstellt":
            # Quiz nach Erstellungsdatum sortieren
            query = "SELECT id, titel FROM quiz ORDER BY id DESC"
            c.execute(query)
            quiz = c.fetchall()
        elif sort_mode == "Noch nie gemacht" and schueler:
            # Quiz, die der Schüler noch nie gemacht hat
            query = """
                SELECT quiz.id, quiz.titel
                FROM quiz
                WHERE quiz.id NOT IN (
                    SELECT quiz_id FROM ergebnis WHERE schueler_id = (SELECT id FROM schueler WHERE name = ?)
                )
            """
            c.execute(query, (schueler,))
            quiz = c.fetchall()
        else:
            # Standard: alle Quiz anzeigen
            query = "SELECT id, titel FROM quiz"
            c.execute(query)
            quiz = c.fetchall()
        self.quiz_list.clear()
        for q in quiz:
            self.quiz_list.addItem(q[1]) # Quiz-Titel zur Liste hinzufügen
        conn.close()

    def start_quiz(self):
        # Quiz starten, QuizDialog öffnen
        schueler = self.schueler_dropdown.currentText()
        quiz_item = self.quiz_list.currentItem()
        if not schueler or not quiz_item:
            QMessageBox.warning(self, "Fehler", "Bitte wähle einen Schüler und ein Quiz aus.")
            return
        # Quiz-ID aus DB holen
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("SELECT id FROM quiz WHERE titel = ?", (quiz_item.text(),))
        quiz_row = c.fetchone()
        conn.close()
        if not quiz_row:
            QMessageBox.warning(self, "Fehler", "Quiz nicht gefunden.")
            return
        quiz_id = quiz_row[0]
        # QuizDialog anzeigen, Ergebnis wird nach Schließen nicht erneut angezeigt
        dialog = QuizDialog(schueler, quiz_id, quiz_item.text())
        dialog.exec()

class QuizScoreWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Quiz-Score Übersicht")
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # Übersicht: Anzahl beantworteter Fragen
        self.score_label = QLabel()
        self.layout.addWidget(self.score_label)
        self.update_score_overview()

        # Button: Fragen anzeigen
        self.btn_show_questions = QPushButton("Fragen anzeigen")
        self.btn_show_questions.clicked.connect(self.show_questions)
        self.layout.addWidget(self.btn_show_questions)

        # Button: Neue Frage erstellen
        self.btn_new_question = QPushButton("Neue Frage erstellen")
        self.btn_new_question.clicked.connect(self.create_new_question)
        self.layout.addWidget(self.btn_new_question)

        # Button: Beenden & Git
        self.btn_quit = QPushButton("Beenden & Git")
        self.btn_quit.clicked.connect(self.quit_and_git)
        self.layout.addWidget(self.btn_quit)

    #def update_score_overview(self):
     #   conn = sqlite3.connect(DB_PATH) # Zugriff auf globalen DB_PATH
      #  c = conn.cursor()
       # # Anzahl beantworteter Fragen (Summe aller gegebene_antwort)
       # c.execute("SELECT COUNT(*) FROM gegebene_antwort")
       # count = c.fetchone()[0]
       # conn.close()
       # self.score_label.setText(f"Beantwortete Fragen: {count}")
#TODO: ändern auf json lokal speichern und laden statt in der datenbank

    def show_questions(self):
        # Zeigt alle Fragen mit Antwortmöglichkeiten in einem Dialog
        # Redundante lokale Imports entfernt, um globalen DB_PATH zu verwenden
        conn = sqlite3.connect(DB_PATH) 
        c = conn.cursor()
        c.execute("SELECT frage.id, frage.frage_text FROM frage")
        fragen = c.fetchall()
        dialog = QDialog(self)
        dialog.setWindowTitle("Alle Fragen anzeigen")
        layout = QVBoxLayout(dialog)
        for frage_id, frage_text in fragen:
            layout.addWidget(QLabel(f"Frage: {frage_text}"))
            c.execute("SELECT antwort_text FROM antwort WHERE frage_id = ?", (frage_id,))
            antworten = c.fetchall()
            for antwort_text, in antworten:
                layout.addWidget(QLabel(f"Antwort: {antwort_text}"))
        conn.close()
        btn_close = QPushButton("Schließen")
        btn_close.clicked.connect(dialog.accept)
        layout.addWidget(btn_close)
        dialog.exec()

    def create_new_question(self):
        # Dialog zum Erstellen einer neuen Frage
        dialog = QDialog(self)
        dialog.setWindowTitle("Neue Frage erstellen")
        layout = QVBoxLayout(dialog)
        frage_input = QLineEdit()
        layout.addWidget(QLabel("Fragetext:"))
        layout.addWidget(frage_input)
        antwort_inputs = []
        for i in range(4):
            antwort_input = QLineEdit()
            layout.addWidget(QLabel(f"Antwort {i+1}:"))
            layout.addWidget(antwort_input)
            antwort_inputs.append(antwort_input)
        richtig_dropdown = QComboBox()
        richtig_dropdown.addItems(["Antwort 1", "Antwort 2", "Antwort 3", "Antwort 4"])
        layout.addWidget(QLabel("Richtige Antwort wählen:"))
        layout.addWidget(richtig_dropdown)
        btn_save = QPushButton("Speichern")
        layout.addWidget(btn_save)
        btn_cancel = QPushButton("Abbrechen")
        layout.addWidget(btn_cancel)
        def save_question():
            frage_text = frage_input.text().strip()
            antworten = [a.text().strip() for a in antwort_inputs]
            richtig_index = richtig_dropdown.currentIndex()
            if not frage_text or not all(antworten):
                QMessageBox.warning(dialog, "Fehler", "Bitte alle Felder ausfüllen.")
                return
            
            # Redundante lokale Imports entfernt, um globalen DB_PATH zu verwenden
            conn = sqlite3.connect(DB_PATH)
            c = conn.cursor()
            
            # Annahme: Alle neuen Fragen gehören zum Quiz mit ID 1
            c.execute("INSERT INTO frage (frage_text, quiz_id) VALUES (?, 1)", (frage_text,))
            frage_id = c.lastrowid
            for idx, antwort_text in enumerate(antworten):
                ist_richtig = 1 if idx == richtig_index else 0
                c.execute("INSERT INTO antwort (antwort_text, frage_id, ist_richtig) VALUES (?, ?, ?)", (antwort_text, frage_id, ist_richtig))
            conn.commit()
            conn.close()
            QMessageBox.information(dialog, "Erfolg", "Frage wurde gespeichert.")
            dialog.accept()
            self.update_score_overview()
        btn_save.clicked.connect(save_question)
        btn_cancel.clicked.connect(dialog.reject)
        dialog.exec()

    def quit_and_git(self):
        # Fenster schließen und Git-Push ausführen (einheitlich aus main.py)
        git_push()
        self.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = QuizScoreWindow()
    window.show()
    sys.exit(app.exec())
