from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QPushButton, QVBoxLayout,
    QHBoxLayout, QLabel, QInputDialog, QLineEdit, QFrame
)
from PySide6.QtCore import QTimer, Qt
from PySide6.QtWidgets import QMessageBox
import sys
from news.news_main import get_news, delete_old_news, add_news_item
# Quotes-Import
from quotes.quotes_main import get_quotes, add_quotes as add_quote_item
from counter.counter_main import CounterDialog
from password.password_main import PasswordWindow
from quiz.quiz_main import QuizMainWindow
from utils.git_utils import git_pull, git_push, git_merge
from attendance_calendar.date_attendance_main import AttendanceCalendar
from Elekrotechnick.gui import ElektroGUI
# Zahlensysteme-Funktionen (nur Quiz-Funktionen verwenden, GUI nicht verändern)
from zahlensysteme.main.fuctions import (
    binaer_zu_dezi,
    dezi_zu_binaer,
    dezi_zu_hexadezi,
    hexadezi_zu_dezi,
)


class NewsFenster(QWidget):
    def __init__(self):
        super().__init__()
        self.news_list = get_news()
        
        # Fallback für leere Liste
        if not self.news_list:
            self.news_list = ["Keine News vorhanden. Klicke 'Neu' um eine zu erstellen."]
        
        self.current_index = 0
        
        layout = QVBoxLayout()
        self.label = QLabel(self.news_list[self.current_index])
        self.label.setWordWrap(True)
        layout.addWidget(self.label)

        button_layout = QHBoxLayout()
        btn_prev = QPushButton("Zurück")
        btn_prev.clicked.connect(self.show_prev)
        btn_new = QPushButton("Neu")
        btn_new.clicked.connect(self.add_news)
        btn_next = QPushButton("Nächste")
        btn_next.clicked.connect(self.show_next_immediately)
        button_layout.addWidget(btn_prev)
        button_layout.addWidget(btn_new)
        button_layout.addWidget(btn_next)
        layout.addLayout(button_layout)
        self.setLayout(layout)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.show_next)
        self.timer.start(45000)  # 45 Sekunden

    def show_next(self):
        if len(self.news_list) <= 1:
            return  # Kein Weiterschalten wenn nur 1 Eintrag
        self.current_index = (self.current_index + 1) % len(self.news_list)
        self.label.setText(self.news_list[self.current_index])

    def show_prev(self):
        if len(self.news_list) <= 1:
            return  # Kein Zurückschalten wenn nur 1 Eintrag
        self.current_index = (self.current_index - 1) % len(self.news_list)
        self.label.setText(self.news_list[self.current_index])

    def show_next_immediately(self):
        self.timer.stop()
        self.show_next()
        self.timer.start(45000)

    def reload_news(self):
        self.news_list = get_news()
        
        # Fallback für leere Liste
        if not self.news_list:
            self.news_list = ["Keine News vorhanden."]
        
        # Index zurücksetzen wenn außerhalb der neuen Liste
        if self.current_index >= len(self.news_list):
            self.current_index = 0
        
        self.label.setText(self.news_list[self.current_index])

    def add_news(self):
        text, ok = QInputDialog.getText(self, "Neue News", "News-Text eingeben:", QLineEdit.Normal)
        if ok and text.strip():
            try:
                from datetime import datetime
                created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                add_news_item(text, "news/news.db", created_at)
                self.reload_news()
            except Exception as e:
                print(f"Fehler beim Hinzufügen: {e}")
                self.label.setText(f"Fehler: {e}")

class QuotesFenster(QWidget):
    def __init__(self):
        super().__init__()
        self.quotes_list = get_quotes()
        self.current_index = 0

        layout = QVBoxLayout()
        self.label = QLabel(self.quotes_list[self.current_index])
        self.label.setWordWrap(True)
        layout.addWidget(self.label)

        button_layout = QHBoxLayout()
        btn_prev = QPushButton("Zurück")
        btn_prev.clicked.connect(self.show_prev)
        btn_new = QPushButton("Neu")
        btn_new.clicked.connect(self.add_quote)
        btn_next = QPushButton("Nächste")
        btn_next.clicked.connect(self.show_next_immediately)
        button_layout.addWidget(btn_prev)
        button_layout.addWidget(btn_new)
        button_layout.addWidget(btn_next)
        layout.addLayout(button_layout)
        self.setLayout(layout)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.show_next)
        self.timer.start(45000)  # 45 Sekunden

    def show_prev(self):
        self.current_index = (self.current_index - 1) % len(self.quotes_list)
        self.label.setText(self.quotes_list[self.current_index])

    def show_next(self):
        self.current_index = (self.current_index + 1) % len(self.quotes_list)
        self.label.setText(self.quotes_list[self.current_index])

    def show_next_immediately(self):
        self.timer.stop()
        self.show_next()
        self.timer.start(45000)

    def reload_quotes(self):
        self.quotes_list = get_quotes()
        self.label.setText(self.quotes_list[self.current_index])

    def add_quote(self):
        text, ok = QInputDialog.getText(self, "Neues Zitat", "Zitat-Text eingeben:", QLineEdit.Normal)
        if ok and text.strip():
            add_quote_item(text, "quotes/quotes.db")
            git_push()
            self.reload_quotes()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Verwaltungstool")

        # --- Git- und News-Initialisierung beim Start ---
        git_pull()
        git_merge()
        delete_old_news("news/news.db")
        git_push()

        main_widget = QWidget()
        main_layout = QVBoxLayout()

        # Obere Buttons
        top_layout = QHBoxLayout()

        btn_anwesenheit = QPushButton("Anwesenheitskalender")
        btn_anwesenheit.clicked.connect(self.oeffne_anwesenheit)
        top_layout.addWidget(btn_anwesenheit)

        btn_counter = QPushButton("Störungs Counter")
        btn_counter.clicked.connect(self.oeffne_counter)
        top_layout.addWidget(btn_counter)

        btn_quizscore = QPushButton("Quiz starten")
        btn_quizscore.clicked.connect(self.oeffne_quizscore)
        top_layout.addWidget(btn_quizscore)

        # Neuer Button für Zahlensysteme zwischen Quiz und Passwortgenerator
        btn_zahlensysteme = QPushButton("Zahlensysteme")
        btn_zahlensysteme.clicked.connect(self.oeffne_zahlensysteme)
        top_layout.addWidget(btn_zahlensysteme)

        btn_elektro = QPushButton("Elektrotechnik")
        btn_elektro.clicked.connect(self.oeffne_elektrotechnik)
        top_layout.addWidget(btn_elektro)

        btn_password = QPushButton("Passwortgenerator")
        btn_password.clicked.connect(self.oeffne_password)
        top_layout.addWidget(btn_password)
        
        main_layout.addLayout(top_layout)

        # Mittlere Info-Fenster
        middle_layout = QHBoxLayout()
        self.news_fenster = NewsFenster()
        self.quotes_fenster = QuotesFenster()
        middle_layout.addWidget(self.news_fenster)
        middle_layout.addWidget(self.quotes_fenster)
        main_layout.addLayout(middle_layout)

        # Untere Buttons
        bottom_layout = QHBoxLayout()
        # Branding-Box unten links
        branding_layout = QHBoxLayout()
        branding_frame = QFrame()
        branding_frame.setStyleSheet("background-color: white; border: 1px solid #ccc;")
        branding_inner = QHBoxLayout()
        logo = QLabel()
        logo.setFixedSize(15, 15)
        logo.setStyleSheet("background-color: #bbb; border: 1px solid #888;")  # Platzhalter für Logo
        branding_inner.addWidget(logo)
        branding_text = QLabel("MAKE BY UMSCHULUNGS GRUPPE FROM 03.2025-03.2027")
        branding_inner.addWidget(branding_text)
        branding_frame.setLayout(branding_inner)
        branding_layout.addWidget(branding_frame)
        branding_layout.addStretch()
        bottom_layout.addLayout(branding_layout)

        bottom_layout.addStretch()
        btn_beenden = QPushButton("Beenden")
        btn_beenden.clicked.connect(self.beenden)
        bottom_layout.addWidget(btn_beenden)
        btn_aktualisieren = QPushButton("Aktualisieren")
        btn_aktualisieren.clicked.connect(self.git_update)
        bottom_layout.addWidget(btn_aktualisieren)
        main_layout.addLayout(bottom_layout)

        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)

        # Timer für automatisches Git Pull alle 60 Sekunden
        self.git_timer = QTimer(self)
        self.git_timer.timeout.connect(self.git_auto_pull)
        self.git_timer.start(60000)  #TODO: wieder auf 60 Sekunden ändern
    
    def oeffne_anwesenheit(self):
        self.anwesenheit_window = AttendanceCalendar()
        self.anwesenheit_window.show()

    def oeffne_counter(self):
        dialog = CounterDialog(self)
        dialog.exec()

    def oeffne_password(self):
        self.password_window = PasswordWindow()
        self.password_window.show()

    def oeffne_quizscore(self):
        self.quiz_window = QuizMainWindow()
        self.quiz_window.show()

    def oeffne_elektrotechnik(self):
        self.elektro_window = ElektroGUI()
        self.elektro_window.show()

    def git_update(self):
        git_pull()
        git_merge()
        self.news_fenster.reload_news()

    def git_auto_pull(self):
        git_pull()
        self.news_fenster.reload_news()

    def ask_and_check(self, module, parent=None):
        try:
            prompt, answer, input_type = module.get_quiz()
        except Exception as e:
            QMessageBox.warning(parent or self, "Fehler", f"Quiz kann nicht geladen werden: {e}")
            return

        text, ok = QInputDialog.getText(parent or self, "Quiz", prompt)
        if not ok:
            return
        if input_type == 'int':
            try:
                user = int(text)
            except ValueError:
                QMessageBox.warning(parent or self, "Fehler", "Bitte eine Zahl eingeben!")
                return
            correct = (user == answer)
        else:
            user = text.strip().upper()
            correct = (user == str(answer).upper())

        if correct:
            QMessageBox.information(parent or self, "Ergebnis", "Richtig!")
        else:
            QMessageBox.information(parent or self, "Ergebnis", f"Falsch! Richtig wäre: {answer}")

    def oeffne_zahlensysteme(self):
        # Erstellt ein eingebettetes Fenster für die Zahlensystem-Tools (verwendet vorhandene get_quiz)
        self.zahl_window = QWidget()
        self.zahl_window.setWindowTitle("Zahlensysteme")
        layout = QVBoxLayout()

        btn1 = QPushButton("Binär -> Dezimal")
        btn2 = QPushButton("Dezimal -> Binär")
        btn3 = QPushButton("Dezimal -> Hexadezimal")
        btn4 = QPushButton("Hexadezimal -> Dezimal")
        btn5 = QPushButton("Beenden")

        btn1.clicked.connect(lambda: self.ask_and_check(binaer_zu_dezi, self.zahl_window))
        btn2.clicked.connect(lambda: self.ask_and_check(dezi_zu_binaer, self.zahl_window))
        btn3.clicked.connect(lambda: self.ask_and_check(dezi_zu_hexadezi, self.zahl_window))
        btn4.clicked.connect(lambda: self.ask_and_check(hexadezi_zu_dezi, self.zahl_window))
        btn5.clicked.connect(self.zahl_window.close)

        for btn in (btn1, btn2, btn3, btn4, btn5):
            layout.addWidget(btn)

        self.zahl_window.setLayout(layout)
        self.zahl_window.show()

    def beenden(self):
        git_push()
        QApplication.quit()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


    #TODO: funktionen auslagern in eigene dateien