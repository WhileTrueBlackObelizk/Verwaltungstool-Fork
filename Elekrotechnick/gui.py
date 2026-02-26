from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
import random
import os
import sys
import json

# Funktionen aus dem Modul importieren
from Elekrotechnick.main import prüfe_antwort


class ElektroGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Elektrotechnik Übung")
        self.setGeometry(100, 100, 700, 650)
        
        # Aufgaben laden
        self.aufgaben = self._lade_aufgaben()
        self.aktuelles = None
        self.png_ordner = os.path.join(os.path.dirname(__file__), "PNG_e.aufgaben")
        
        # Layout
        layout = QVBoxLayout()
        
        self.image_label = QLabel("Keine Aufgabe ausgewählt")
        self.image_label.setMinimumHeight(350)
        self.image_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.image_label)
        
        layout.addSpacing(10)
        
        self.entry = QLineEdit()
        self.entry.setPlaceholderText("Ergebnis eingeben...")
        layout.addWidget(self.entry)
        
        self.check_button = QPushButton("Antwort prüfen")
        self.check_button.clicked.connect(self.check_answer)
        layout.addWidget(self.check_button)
        
        self.new_button = QPushButton("Neue Aufgabe")
        self.new_button.clicked.connect(self.neue_aufgabe)
        layout.addWidget(self.new_button)
        
        self.setLayout(layout)
    
    def _lade_aufgaben(self):
        """Lädt die Aufgabendaten aus der nicht_schummeln.json"""
        json_datei = os.path.join(os.path.dirname(__file__), "nicht_schummeln.json")
        try:
            with open(json_datei, "r", encoding="utf-8") as f:
                daten = json.load(f)
                return daten.get("aufgaben", [])
        except FileNotFoundError:
            print(f"Fehler: {json_datei} nicht gefunden!")
            return []
    
    def _zeige_png(self, png_dateiname):
        """Zeigt das PNG-Bild in Originalgröße an"""
        png_pfad = os.path.join(self.png_ordner, png_dateiname)
        if os.path.exists(png_pfad):
            pixmap = QPixmap(png_pfad)
            # Maximalbreite setzen, aber Seitenverhältnis beibehalten
            max_width = 650
            if pixmap.width() > max_width:
                pixmap = pixmap.scaledToWidth(max_width, Qt.SmoothTransformation)
            self.image_label.setPixmap(pixmap)
        else:
            self.image_label.setText(f"Bild nicht gefunden: {png_dateiname}")
    
    def neue_aufgabe(self):
        if not self.aufgaben:
            QMessageBox.critical(self, "Fehler", "Keine Aufgaben vorhanden.")
            return
        self.aktuelles = random.choice(self.aufgaben)
        self._zeige_png(self.aktuelles['png'])
        self.entry.clear()
        self.entry.setFocus()
    
    def check_answer(self):
        if not self.aktuelles:
            QMessageBox.information(self, "Info", "Bitte zuerst eine Aufgabe auswählen.")
            return
        antwort = self.entry.text().strip()
        richtig = prüfe_antwort(self.aktuelles['id'], antwort)
        if richtig:
            QMessageBox.information(self, "Ergebnis", "Richtig!")
        else:
            QMessageBox.information(self, "Ergebnis", "Falsch!")

