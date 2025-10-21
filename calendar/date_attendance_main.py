"""
Ein kleines Tool, um die eigene Anwesenheit in einem Kalender zu erfassen.

Statusoptionen:
- Karlsruhe
- Homeoffice
- Urlaub
- Krankheit
- Feiertag

Die Daten werden lokal in einer JSON-Datei gespeichert.
Markierte Tage werden farblich hervorgehoben.
"""

import sys
import json
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QComboBox, QLabel, QCalendarWidget
from PySide6.QtCore import QDate
from PySide6.QtGui import QTextCharFormat, QColor

# Name der JSON-Datei für die Speicherung
CLASS_JSON_FILE = "meine_anwesenheit.json"

class AttendanceCalendar(QWidget):
    """
    Hauptfenster für die Anwesenheitsverwaltung.
    Zeigt einen Kalender, erlaubt die Auswahl eines Status pro Tag
    und speichert die Daten in einer JSON-Datei.
    """

    # Statusoptionen und ihre zugehörigen Farben
    STATUS_COLORS = {
        "Karlsruhe": "lightgreen",
        "Homeoffice": "lightyellow",#etwas verdunkeln
        "Urlaub": "lightblue",
        "Krankheit": "lightcoral",
        "Feiertag": "lightgray"
    }

    STATUS_OPTIONS = list(STATUS_COLORS.keys())

    def __init__(self):
        """Initialisiert das Fenster, Widgets und lädt die gespeicherten Daten."""
        super().__init__()
        self.setWindowTitle("Meine Anwesenheit")
        self.resize(400, 300)

        # Kalender-Widget
        self.calendar = QCalendarWidget(self)
        self.calendar.setGridVisible(True)

        # Label für Anzeige des Status des ausgewählten Datums
        self.status_label = QLabel("", self)

        # Dropdown zur Auswahl des Status
        self.combo = QComboBox(self)
        self.combo.addItems(self.STATUS_OPTIONS)

        # Button zum Setzen des Status
        self.save_button = QPushButton("Status setzen", self)
        self.save_button.clicked.connect(self.set_status_for_selected_date)

        # Layout erstellen und Widgets hinzufügen
        layout = QVBoxLayout(self)
        layout.addWidget(self.calendar)
        layout.addWidget(self.status_label)
        layout.addWidget(self.combo)
        layout.addWidget(self.save_button)
        self.setLayout(layout)

        # Daten laden
        self.attendance = self.load_data()

        # Bei Klick auf Datum Status anzeigen
        self.calendar.clicked.connect(self.on_date_clicked)

        # Bereits gespeicherte Tage beim Start markieren
        self.highlight_saved_days()

    def load_data(self) -> dict:
        """
        Lädt die gespeicherten Anwesenheitsdaten aus der JSON-Datei.

        Returns:
            dict: Dictionary im Format {"YYYY-MM-DD": "Status", ...}
        """
        try:
            with open(CLASS_JSON_FILE, "r") as f:
                data = json.load(f)
            return data
        except FileNotFoundError:
            # Datei existiert noch nicht
            return {}

    def save_data(self):
        """Speichert die aktuellen Anwesenheitsdaten in die JSON-Datei."""
        with open(CLASS_JSON_FILE, "w") as f:
            json.dump(self.attendance, f, indent=2, ensure_ascii=False)

    def on_date_clicked(self, qdate: QDate):
        """
        Wird aufgerufen, wenn ein Datum im Kalender angeklickt wird.
        Zeigt den aktuellen Status für dieses Datum an.

        Args:
            qdate (QDate): Ausgewähltes Datum
        """
        date_str = qdate.toString("yyyy-MM-dd")
        status = self.attendance.get(date_str, None)
        if status:
            self.status_label.setText(f"Status am {date_str}: {status}")
        else:
            self.status_label.setText(f"Kein Status für {date_str} gesetzt")

    def set_status_for_selected_date(self):
        """
        Setzt den gewählten Status für das aktuell ausgewählte Datum.
        Speichert die Daten und markiert den Tag farblich.
        """
        qdate = self.calendar.selectedDate()
        date_str = qdate.toString("yyyy-MM-dd")
        status = self.combo.currentText()
        self.attendance[date_str] = status
        self.save_data()
        self.status_label.setText(f"Status am {date_str}: {status}")
        self.highlight_day(qdate, status)

    def highlight_day(self, qdate: QDate, status: str):
        """
        Markiert einen einzelnen Tag im Kalender mit der entsprechenden Farbe.

        Args:
            qdate (QDate): Zu markierendes Datum
            status (str): Status des Tages (entsprechend STATUS_COLORS)
        """
        fmt = QTextCharFormat()
        color = self.STATUS_COLORS.get(status, "white")
        fmt.setBackground(QColor(color))
        self.calendar.setDateTextFormat(qdate, fmt)

    def highlight_saved_days(self):
        """
        Markiert alle bereits gespeicherten Tage im Kalender
        entsprechend dem gespeicherten Status.
        """
        for date_str, status in self.attendance.items():
            qdate = QDate.fromString(date_str, "yyyy-MM-dd")
            if qdate.isValid():
                self.highlight_day(qdate, status)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = AttendanceCalendar()
    win.show()
    sys.exit(app.exec())

#TODO:optionen angeben 
#TODO:auswahl funktionalität ändern