import json
from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QComboBox, QLabel, QCalendarWidget
from PySide6.QtCore import QDate
from PySide6.QtGui import QTextCharFormat, QColor
from collections import Counter
from datetime import datetime

CLASS_JSON_FILE = "meine_anwesenheit.json"

class AttendanceCalendar(QWidget):
    """
    Ein Kalender-Widget zur Erfassung persönlicher Anwesenheit.
    Status: Karlsruhe, Homeoffice, Urlaub, Krankheit, Feiertag.
    """

    STATUS_COLORS = {
        "Karlsruhe": "lightgreen",
        "Homeoffice": "#f7f78a",
        "Urlaub": "lightblue",
        "Krankheit": "lightcoral",
        "Feiertag": "lightgray"
    }

    STATUS_OPTIONS = list(STATUS_COLORS.keys())

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Meine Anwesenheit")
        self.resize(420, 350)

        # Widgets
        self.calendar = QCalendarWidget()
        self.calendar.setGridVisible(True)
        self.status_label = QLabel()
        self.combo = QComboBox()
        self.combo.addItems(self.STATUS_OPTIONS)
        self.save_button = QPushButton("Status setzen")

        # Neue Anzeige für Anwesenheitsquote
        self.stats_label = QLabel()
        self.stats_label.setStyleSheet("color: gray; font-size: 11px; margin-top: 4px;")

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.calendar)
        layout.addWidget(self.status_label)
        layout.addWidget(self.combo)
        layout.addWidget(self.save_button)
        layout.addWidget(self.stats_label)
        self.setLayout(layout)

        # Signals
        self.save_button.clicked.connect(self.set_status_for_selected_date)
        self.calendar.clicked.connect(self.on_date_clicked)

        # Daten laden
        self.attendance = self.load_data()
        self.highlight_saved_days()
        self.update_stats_label()

    def load_data(self):
        try:
            with open(CLASS_JSON_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            return {}

    def save_data(self):
        with open(CLASS_JSON_FILE, "w", encoding="utf-8") as f:
            json.dump(self.attendance, f, indent=2, ensure_ascii=False)

    def on_date_clicked(self, qdate: QDate):
        date_str = qdate.toString("yyyy-MM-dd")
        status = self.attendance.get(date_str)
        self.status_label.setText(f"Status am {date_str}: {status or 'Kein Status gesetzt'}")

    def set_status_for_selected_date(self):
    qdate = self.calendar.selectedDate()
    if not qdate.isValid():
        print(f"Ungültiges Datum: {qdate}")
        return  # nichts speichern

    date_str = qdate.toString("yyyy-MM-dd")
    status = self.combo.currentText()
    self.attendance[date_str] = status
    self.save_data()
    self.status_label.setText(f"Status am {date_str}: {status}")
    self.highlight_day(qdate, status)
    self.update_stats_label()

    def highlight_day(self, qdate: QDate, status: str):
        fmt = QTextCharFormat()
        fmt.setBackground(QColor(self.STATUS_COLORS.get(status, "white")))
        self.calendar.setDateTextFormat(qdate, fmt)

    def highlight_saved_days(self):
        for date_str, status in self.attendance.items():
            qdate = QDate.fromString(date_str, "yyyy-MM-dd")
            if qdate.isValid():
                self.highlight_day(qdate, status)

   def update_stats_label(self):
    """Berechnet die Monatsstatistik und aktualisiert die Anzeige."""
    now = datetime.now()
    year, month = now.year, now.month

    # ---------------------------
    # Ungültige Einträge überspringen
    # ---------------------------
    monthly_entries = {}
    for date_str, status in self.attendance.items():
        try:
            dt = datetime.strptime(date_str, "%Y-%m-%d")
        except ValueError:
            print(f"⚠️ Ungültiges Datum übersprungen: {date_str} → {status}")
            continue
        if dt.year == year and dt.month == month:
            monthly_entries[date_str] = status

    # ---------------------------
    # JSON automatisch bereinigen (optional)
    # ---------------------------
    if len(monthly_entries) != len(self.attendance):
        self.attendance = monthly_entries
        self.save_data()
        print("🔧 Ungültige Einträge aus der JSON entfernt.")

    # ---------------------------
    # Anzeige aktualisieren
    # ---------------------------
    if not monthly_entries:
        self.stats_label.setText("Keine Einträge für diesen Monat.")
        return

    counts = Counter(monthly_entries.values())
    total_days = sum(counts.values())

    stats_text = " / ".join(
        f"{status}: {round((counts.get(status, 0) / total_days) * 100)}%"
        for status in self.STATUS_OPTIONS
        if counts.get(status)
    )

    self.stats_label.setText(f"Anwesenheitsquote ({month:02d}/{year}): {stats_text}")

