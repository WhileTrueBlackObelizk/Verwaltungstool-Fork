from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QPushButton, QVBoxLayout,
    QHBoxLayout, QLabel, QInputDialog, QLineEdit, QFrame, QGridLayout,
    QSizePolicy, QMessageBox
)
from PySide6.QtCore import QTimer, Qt
import sys
from news.news_main import get_news, delete_old_news, add_news_item
from quotes.quotes_main import get_quotes, add_quotes as add_quote_item
from counter.counter_main import CounterDialog
from password.password_main import PasswordWindow
from quiz.quiz_main import QuizMainWindow
from utils.git_utils import git_pull, git_push, git_merge
from attendance_calendar.date_attendance_main import AttendanceCalendar
from Elekrotechnick.gui import ElektroGUI
from zahlensysteme.main.fuctions import (
    binaer_zu_dezi,
    dezi_zu_binaer,
    dezi_zu_hexadezi,
    hexadezi_zu_dezi,
)
from apple_theme import APPLE_STYLESHEET


# ── Hilfsfunktion: Card-Frame ────────────────────────────────────────────────

def make_card(layout_inner: QVBoxLayout) -> QFrame:
    """Gibt einen weißen Card-Frame mit abgerundeten Ecken zurück."""
    frame = QFrame()
    frame.setProperty("card", True)
    frame.setLayout(layout_inner)
    frame.setStyleSheet(
        "QFrame[card='true'] {"
        "  background: white;"
        "  border-radius: 12px;"
        "  padding: 12px;"
        "}"
    )
    return frame


# ── Carousel-Panel (News & Memos) ─────────────────────────────────────────────

class CarouselPanel(QWidget):
    """Wiederverwendbares Rotations-Panel für News und Memos."""
    def __init__(self, title, get_fn, add_fn, dialog_title, dialog_label):
        super().__init__()
        self._get_fn = get_fn
        self._add_fn = add_fn
        self._dialog_title = dialog_title
        self._dialog_label = dialog_label

        self.items = get_fn()
        self.current_index = 0

        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)

        inner = QVBoxLayout()
        inner.setSpacing(8)

        header = QLabel(title)
        header.setStyleSheet("font-size: 15px; font-weight: 600; color: #1C1C1E; background: transparent;")
        inner.addWidget(header)

        self.label = QLabel(self.items[self.current_index])
        self.label.setWordWrap(True)
        self.label.setStyleSheet("color: #3A3A3C; background: transparent; font-size: 13px;")
        self.label.setAlignment(Qt.AlignTop)
        self.label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        inner.addWidget(self.label)
        inner.addStretch()

        btn_row = QHBoxLayout()
        btn_row.setSpacing(6)

        btn_prev = QPushButton("‹")
        btn_prev.setFixedSize(32, 32)
        btn_prev.setStyleSheet(
            "QPushButton { background: #E5E5EA; color: #1C1C1E; border-radius: 8px; "
            "font-size: 16px; border: none; }"
            "QPushButton:hover { background: #D1D1D6; }"
        )
        btn_prev.clicked.connect(self.show_prev)

        btn_next = QPushButton("›")
        btn_next.setFixedSize(32, 32)
        btn_next.setStyleSheet(
            "QPushButton { background: #E5E5EA; color: #1C1C1E; border-radius: 8px; "
            "font-size: 16px; border: none; }"
            "QPushButton:hover { background: #D1D1D6; }"
        )
        btn_next.clicked.connect(self.show_next_immediately)

        btn_new = QPushButton("＋")
        btn_new.setFixedSize(32, 32)
        btn_new.setStyleSheet(
            "QPushButton { background: #007AFF; color: white; border-radius: 8px; "
            "font-size: 16px; border: none; }"
            "QPushButton:hover { background: #0062CC; }"
        )
        btn_new.clicked.connect(self.add_item)

        btn_row.addWidget(btn_prev)
        btn_row.addWidget(btn_next)
        btn_row.addStretch()
        btn_row.addWidget(btn_new)
        inner.addLayout(btn_row)

        outer.addWidget(make_card(inner))

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.show_next)
        self.timer.start(45000)

    def show_next(self):
        if len(self.items) <= 1:
            return
        self.current_index = (self.current_index + 1) % len(self.items)
        self.label.setText(self.items[self.current_index])

    def show_prev(self):
        if len(self.items) <= 1:
            return
        self.current_index = (self.current_index - 1) % len(self.items)
        self.label.setText(self.items[self.current_index])

    def show_next_immediately(self):
        self.timer.stop()
        self.show_next()
        self.timer.start(45000)

    def reload(self):
        self.items = self._get_fn()
        if self.current_index >= len(self.items):
            self.current_index = 0
        self.label.setText(self.items[self.current_index])

    def add_item(self):
        text, ok = QInputDialog.getText(self, self._dialog_title, self._dialog_label, QLineEdit.Normal)
        if ok and text.strip():
            try:
                self._add_fn(text)
                self.reload()
            except Exception as e:
                self.label.setText(f"Fehler: {e}")


# ── Hauptfenster ─────────────────────────────────────────────────────────────

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Verwaltungstool")
        self.setMinimumSize(820, 560)

        # Git-Initialisierung beim Start
        git_pull()
        git_merge()
        delete_old_news("news/news.db")
        git_push()

        root = QWidget()
        root_layout = QVBoxLayout(root)
        root_layout.setContentsMargins(20, 20, 20, 16)
        root_layout.setSpacing(16)

        # ── Titelzeile ────────────────────────────────────────
        title_row = QHBoxLayout()
        title = QLabel("Verwaltungstool")
        title.setStyleSheet(
            "font-size: 20px; font-weight: 700; color: #1C1C1E; background: transparent;"
        )
        title_row.addWidget(title)
        title_row.addStretch()

        btn_update = QPushButton("Aktualisieren")
        btn_update.setFixedHeight(32)
        btn_update.setStyleSheet(
            "QPushButton { background: #E5E5EA; color: #1C1C1E; border-radius: 8px; "
            "padding: 0 14px; font-size: 13px; border: none; }"
            "QPushButton:hover { background: #D1D1D6; }"
        )
        btn_update.clicked.connect(self.git_update)
        title_row.addWidget(btn_update)
        root_layout.addLayout(title_row)

        # ── Modul-Grid (2 × 3) ───────────────────────────────
        MODULE_BUTTONS = [
            ("Anwesenheit",   "📅", self.oeffne_anwesenheit),
            ("Störungszähler","⚠️",  self.oeffne_counter),
            ("Quiz",          "🧠", self.oeffne_quizscore),
            ("Zahlensysteme", "🔢", self.oeffne_zahlensysteme),
            ("Elektrotechnik","⚡", self.oeffne_elektrotechnik),
            ("Passwort",      "🔑", self.oeffne_password),
        ]

        grid = QGridLayout()
        grid.setSpacing(10)
        for idx, (label, icon, slot) in enumerate(MODULE_BUTTONS):
            btn = QPushButton(f"{icon}\n{label}")
            btn.setProperty("module", True)
            btn.setMinimumHeight(70)
            btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            btn.clicked.connect(slot)
            grid.addWidget(btn, idx // 3, idx % 3)

        root_layout.addLayout(grid)

        # ── News + Memos nebeneinander ────────────────────────
        panels = QHBoxLayout()
        panels.setSpacing(12)
        self.news_panel = CarouselPanel(
            "News", get_news,
            lambda text: add_news_item(text),
            "Neue News", "News-Text eingeben:",
        )
        self.memos_panel = CarouselPanel(
            "Memos", get_quotes,
            lambda text: (add_quote_item(text), git_push()),
            "Neues Memo", "Memo-Text eingeben:",
        )
        self.news_panel.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.memos_panel.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        panels.addWidget(self.news_panel)
        panels.addWidget(self.memos_panel)
        root_layout.addLayout(panels, stretch=1)

        # ── Footer ────────────────────────────────────────────
        footer = QHBoxLayout()
        branding = QLabel("Umschulungsgruppe · 03/2025 – 03/2027")
        branding.setStyleSheet("color: #8E8E93; font-size: 11px; background: transparent;")
        footer.addWidget(branding)
        footer.addStretch()

        btn_quit = QPushButton("Beenden")
        btn_quit.setFixedHeight(30)
        btn_quit.setStyleSheet(
            "QPushButton { background: #FF3B30; color: white; border-radius: 8px; "
            "padding: 0 14px; font-size: 13px; border: none; }"
            "QPushButton:hover { background: #CC2F26; }"
        )
        btn_quit.clicked.connect(self.beenden)
        footer.addWidget(btn_quit)
        root_layout.addLayout(footer)

        self.setCentralWidget(root)

        # Auto-Pull alle 60 Sekunden
        self.git_timer = QTimer(self)
        self.git_timer.timeout.connect(self.git_auto_pull)
        self.git_timer.start(60000)

    # ── Slot-Methoden ─────────────────────────────────────────

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
        self.news_panel.reload()

    def git_auto_pull(self):
        git_pull()
        self.news_panel.reload()

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
        self.zahl_window = QWidget()
        self.zahl_window.setWindowTitle("Zahlensysteme")
        layout = QVBoxLayout()
        layout.setSpacing(8)
        layout.setContentsMargins(16, 16, 16, 16)

        for label, module in [
            ("Binär → Dezimal",      binaer_zu_dezi),
            ("Dezimal → Binär",      dezi_zu_binaer),
            ("Dezimal → Hexadezimal",dezi_zu_hexadezi),
            ("Hexadezimal → Dezimal",hexadezi_zu_dezi),
        ]:
            btn = QPushButton(label)
            btn.clicked.connect(lambda _, m=module: self.ask_and_check(m, self.zahl_window))
            layout.addWidget(btn)

        btn_close = QPushButton("Schließen")
        btn_close.setStyleSheet(
            "QPushButton { background: #E5E5EA; color: #1C1C1E; border-radius: 8px; "
            "padding: 8px 18px; border: none; }"
            "QPushButton:hover { background: #D1D1D6; }"
        )
        btn_close.clicked.connect(self.zahl_window.close)
        layout.addSpacing(4)
        layout.addWidget(btn_close)

        self.zahl_window.setLayout(layout)
        self.zahl_window.setMinimumWidth(280)
        self.zahl_window.show()

    def beenden(self):
        git_push()
        QApplication.quit()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet(APPLE_STYLESHEET)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
