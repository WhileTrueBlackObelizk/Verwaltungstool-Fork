#-------------------------------------------------------------------------------------------------
# importe
##-------------------------------------------------------------------------------------------------
import sys
import os
import json
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QDialog, QLabel, QRadioButton, QCheckBox,
    QButtonGroup, QLineEdit, QHBoxLayout, QMessageBox, QComboBox
)
from PySide6.QtCore import Qt

from verwaltungstool.config import settings


#-------------------------------------------------------------------------------------------------
# pfade 
##-------------------------------------------------------------------------------------------------

DB_PATH = settings.FLASHCARDS_DB
SCORES_PATH = settings.FLASHCARDS_JSON


#-------------------------------------------------------------------------------------------------
# code begin 
##-------------------------------------------------------------------------------------------------

def lade_scores():
    """Lade Scores aus JSON-Datei."""
    if not os.path.exists(SCORES_PATH):
        return {}
    with open(SCORES_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def speichere_scores(scores):
    """Speichere Scores in JSON-Datei."""
    with open(SCORES_PATH, "w", encoding="utf-8") as f:
        json.dump(scores, f, indent=2)
#---------------------------------------------------------------------------------------------------------------------------------------------
# Hilfsfunktion: Hole Frage mit höchstem Fehler-Count
#---------------------------------------------------------------------------------------------------------------------------------------------
import sqlite3 #to connect to the database könnte ich nach oben setzen wollte es aber hier haben
def frage_mit_hoechstem_count():
    """Finde die Frage mit dem höchsten Fehler-Count."""
    scores = lade_scores()
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT id, frage_text FROM frage")
    fragen = c.fetchall()
    conn.close()
    # Finde Frage mit höchstem Fehler-Count
    #TODO: implementieren: Regel um zu verhindern, dass die gleiche Frage direkt nacheinander gestellt wird
    max_count = -9999
    beste_frage = None
    for frage_id, frage_text in fragen:
        count = scores.get(str(frage_id), 0)
        if count > max_count:
            max_count = count
            beste_frage = (frage_id, frage_text)
    return beste_frage
##---------------------------------------------------------------------------------------------------------------------------------------------
# hhauptmenü
##---------------------------------------------------------------------------------------------------------------------------------------------
class FlashcardsMainWindow(QWidget):
    """Hauptmenü für das Quiz-Modul."""
    def __init__(self):
        """
        aufbau des Hauptmenüs 

        jeder Button öffnet ein entsprechender datei verbunden die als popup aufgerufen wird

        """
        super().__init__()
        self.setWindowTitle("Quiz Menü")
        #-----------------------------------------------------------
        # menü button steurelemente im quiz hauptmenü <-------------
        #-----------------------------------------------------------
        layout = QVBoxLayout(self)
        self.btn_frage_beantworten = QPushButton("Frage beantworten")
        self.btn_frage_hinzufuegen = QPushButton("Frage hinzufügen")
        layout.addWidget(self.btn_frage_beantworten)
        layout.addWidget(self.btn_frage_hinzufuegen)
        self.btn_frage_beantworten.clicked.connect(self.frage_beantworten)
        self.btn_frage_hinzufuegen.clicked.connect(self.frage_hinzufuegen)

    def frage_beantworten(self):
        """
        öffnet das popup zum beantworten der frage mit dem höchsten fehler count



        """
        frage = frage_mit_hoechstem_count()
        if not frage:
            QMessageBox.information(self, "Info", "Keine Fragen vorhanden.")
            return
        dialog = FrageBeantwortenDialog(frage[0], frage[1], self)
        dialog.exec()

    def frage_hinzufuegen(self):
        """
        öffnet das popup zum hinzufügen einer neuen frage

        """


        dialog = FrageHinzufuegenDialog(self)
        dialog.exec()

#---------------------------------------------------------------------------------------------------------------------------------------------
# Popup zum Beantworten
#---------------------------------------------------------------------------------------------------------------------------------------------
class FrageBeantwortenDialog(QDialog):
    def __init__(self, frage_id, frage_text, parent=None):
        """
        zum beantworten einer frage
        werden dabei die antworten aus der datenbank geladen und als checkboxen angezeigt 
        id wird verwendet um die gegebenene antworten zu zu ordnen 

        """
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
        #------------------
        # Buttons <-------- menü steuerung im fragen beantworten screen
        #------------------
        
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
        """
        wertet die gegebenen antworten aus und zeigt eine nachricht an ob die antwort richtig oder falsch war
        aktualisiert den score in der json datei entsprechend
        lädt die nächste frage mit dem höchsten fehler count wenn der weiter button erneut gedrückt wird

        fehler count kann negativ sein wenn die frage oft richtig beantwortet wurde um sie seltener zu zeigen
        """
        #TODO: implementieren einer regel die dafür sorgt das eine frage die man gerade falsch beantwortet hat nur weil sie die ist die den hösten count hat wieder vorgeschlagen wird sonder mindeten 1 andere frage kamm damit es nicht zu einfach ist 
        #getestet funktioniert

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
            scores[frage_id_str] = scores.get(frage_id_str, 0) - 1 # richtig antwort reduziert das auf kommen der frage 
        else:
            QMessageBox.warning(self, "Falsch!", f"Falsch beantwortet! Richtige Antwort(en):\n" + self.richtige_antworten_text())
            scores[frage_id_str] = scores.get(frage_id_str, 0) + 1 # falsche antwort erhöt die häfigkeit der fragen in der routation 
        speichere_scores(scores)
        self.auswertung_gemacht = True
        self.btn_weiter.setText("Weiter zur nächsten Frage")# button steuert: zwischen den fragen wechseln (antworten auswerten und nächste frage laden, richtige antworten anzeigen )

    def richtige_antworten_text(self):
        """
        Gibt die richtigen Antworten als Text zurück.
        für den lernefeffekt hat man unbegrenze zeit die richtige antwort zu lesen 
        """
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("SELECT antwort_text FROM antwort WHERE frage_id = ? AND ist_richtig = 1", (self.frage_id,))
        richtige = [row[0] for row in c.fetchall()]
        conn.close()
        return "\n".join(richtige) # richtige antworten als text zurückgeben für lerneffekt

    def frage_bearbeiten(self):
        """
        steuert die möglichkeit die möglichkeit die frage zu bearbeiten
        """
        #TODO: testen ob die frage bearbeitung funktioniert ""geht" /testen ob der wert des count neu gesetzt wird nach dem bearbeiten der frage "offen"

        dialog = FrageBearbeitenDialog(self.frage_id, self)
        dialog.exec()

#---------------------------------------------------------------------------------------------------------------------------------------------
# Dialog zum Bearbeiten einer Frage
#---------------------------------------------------------------------------------------------------------------------------------------------
class FrageBearbeitenDialog(QDialog):
    def __init__(self, frage_id, parent=None):
        """
        hier können frage und antworten bearbeitet werden 
        wichtig: id wird verwendet um die frage und antworten in der datenbank zu finden und zu aktualisieren
        bedenken: änderungen werden direkt in der datenbank gespeichert beim klicken auf speichern

        """
        #TODO implementieren git automatik für DB
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
        """
        speichert die änderungen in der datenbank
        wichtig: id wird verwendet um die frage und antworten in der datenbank zu finden und zu aktualisieren
        denke dran git push wird aufzurufen nach dem speichern um die änderungen für alle nutzer verfügbar zu machen
        """
        #TODO: implementieren einer git push funktion nach dem speichern

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

#---------------------------------------------------------------------------------------------------------------------------------------------
# idialog zum Hinzufügen einer neuen Frage
#---------------------------------------------------------------------------------------------------------------------------------------------
class FrageHinzufuegenDialog(QDialog):
    """Dialog zum Hinzufügen einer neuen Frage."""
    def __init__(self, parent=None):
        """
        initialisiert den dialog zum hinzufügen einer neuen frage
        4 antworten maximal
        mindestens 2 antworten erforderlich
        mindestens eine antwort muss als richtig markiert sein
        maximal 4 richtige antworten erlau bt 
        """
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
        """
        speichert die neue frage in der datenbank
        wichtig: neue id wird automatisch generiert
        git push wird automatisch aufgerufen nach dem speichern um die änderungen für alle nutzer verfügbar zu machen

        achtung: es dürfen nur maximal 4 antworten hinzugefügt werden
        mindestens 2 antworten müssen hinzugefügt werden
        mindestens eine antwort muss als richtig markiert sein
        maximal 4 richtige antworten erlaubt

        mögliche eingabe fehler werden abgefangen und entsprechende nachrichten angezeigt
        bei fehler im fragen aufbau ist fragen bearbeiten implementiert um die frage später zu korrigieren
        """
        frage_text = self.frage_input.text().strip()
        antworten = [inp.text().strip() for inp in self.antwort_inputs if inp.text().strip()]
        richtig = [chk.isChecked() for chk in self.richtig_checks][:len(antworten)]
        if not frage_text or len(antworten) < 2:
            QMessageBox.warning(self, "Fehler", "Mindestens 2 Antworten und Fragetext erforderlich.")#<-----fehler text 1
            return
        if not any(richtig):
            QMessageBox.warning(self, "Fehler", "Mindestens eine Antwort muss als richtig markiert sein.")#<-----fehler text 2
            return
        if len(antworten) > 4:
            QMessageBox.warning(self, "Fehler", "Maximal 4 Antworten erlaubt.") #<-----fehler text 3
            return
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        #-------------------
        #  ID   <-----------
        #-------------------
        c.execute("SELECT MAX(id) FROM frage")
        max_id = c.fetchone()[0]
        neue_id = int(max_id)+1 if max_id else 1#höste vergebene id plus 1 = neue id 
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
