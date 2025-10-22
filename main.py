from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QPushButton, QVBoxLayout,
    QHBoxLayout, QLabel, QInputDialog, QLineEdit, QFrame
)
from PySide6.QtCore import QTimer, Qt
import sys
from news.news_main import get_news, delete_old_news, add_news_item
# Quotes-Import
from quotes.quotes_main import get_quotes, add_quotes as add_quote_item
from counter.counter_main import CounterDialog
from password.password_main import PasswordWindow
from quiz.quiz_main import QuizScoreWindow
from utils.git_utils import git_pull, git_push, git_merge
from attendance_calendar.date_attendance_main import AttendanceCalendar


class NewsFenster(QWidget):
    def __init__(self):
        super().__init__()
        self.news_list = get_news()
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

    def show_prev(self):
        self.current_index = (self.current_index - 1) % len(self.news_list)
        self.label.setText(self.news_list[self.current_index])

    def show_next(self):
        self.current_index = (self.current_index + 1) % len(self.news_list)
        self.label.setText(self.news_list[self.current_index])

    def show_next_immediately(self):
        self.timer.stop()
        self.show_next()
        self.timer.start(45000)

    def reload_news(self):
        self.news_list = get_news()
        self.current_index = 0
        self.label.setText(self.news_list[self.current_index])

    def add_news(self):
        text, ok = QInputDialog.getText(self, "Neue News", "News-Text eingeben:", QLineEdit.Normal)
        if ok and text.strip():
            from datetime import datetime
            created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            # add_news_item erwartet (text, db_path), ggf. anpassen!
            add_news_item(text, "news/news.db", created_at)
            git_push()
            self.reload_news()

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

        btn_quizscore = QPushButton("Quiz-Score Übersicht")
        btn_quizscore.clicked.connect(self.oeffne_quizscore)
        top_layout.addWidget(btn_quizscore)

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
        self.git_timer.start(60000000000)  #TODO: wieder auf 60 Sekunden ändern
    
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
        self.quizscore_window = QuizScoreWindow()
        self.quizscore_window.show()

    def git_update(self):
        git_pull()
        git_merge()
        self.news_fenster.reload_news()

    def git_auto_pull(self):
        git_pull()
        self.news_fenster.reload_news()

    def beenden(self):
        git_push()
        QApplication.quit()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


    #TODO: funktionen auslagern in eigene dateien