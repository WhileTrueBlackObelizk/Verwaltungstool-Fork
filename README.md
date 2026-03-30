**Verwaltungstool**
Dieses Verwaltungstool wurde entwickelt, um sämtliche organisatorische Aufgaben während einer Umschulung effizient und übersichtlich zu gestalten. Ziel ist es, alle bisher genutzten Einzeltools in einer zentralen Anwendung zusammenzuführen und sowohl Verwaltungs-, Hilfs- und Lernfunktionen bereitzustellen.

Teamgröße: Variiert (Anzahl der Umschüler)

---

**Funktionsübersicht**
🛠 Verwaltungstools
Planungskalender (Anwesenheit): Erstellt ein Raster basierend auf dem aktuellen Datum. Ermöglicht das Tracking von Anwesenheiten und Berichten.

**Features**: Vorheriger/Nächster Monat, Duplikaterkennung, Listenabgleich und prozentuale Übersicht der vorhandenen Berichte.

**Passwortgenerator**: Erstellt Passwörter nach festen Regeln für unkritische Plattformen. Inklusive lokaler, verschlüsselter Speicherung (Master-Passwort erforderlich).

**Störungscounter**: Erfassung technischer oder allgemeiner Störungen während der Umschulungsdauer zur statistischen Auswertung.

**Hilfs- und Lerntools**
**Netzplan-Übungsprogramm**: Tool zum händischen Zeichnen und anschließenden Kontrollieren von Netzplänen – ideal für die Prüfungsvorbereitung.

**Lernkarten für AP2**: Speziell auf die Abschlussprüfung 2 zugeschnittene digitale Karteikarten.

**Quiz**: Zufällige Lerneinheiten zu IT-Inhalten mit 2–4 Antwortmöglichkeiten, Auswertung und lokalem Fortschritts-Tracking.

**Zahlensysteme**: Interaktives Training zur Umrechnung zwischen Binär-, Hexadezimal- und Dezimalsystemen.

**News-Anzeige**: Kurzmitteilungen zum Kursgeschehen, die automatisiert über GitHub verteilt werden (Sichtbarkeit ca. 2 Wochen).

**Merksätze**: Rotierende Anzeige wichtiger Zitate und Merksätze (Wechsel alle 120 Sekunden).

---

**Technische Umsetzung & Voraussetzungen**
Systemvoraussetzungen
Das Tool basiert auf Python 3.10+. Folgende Bibliotheken müssen installiert sein (siehe requirements.txt):

**GUI-Framework**: PySide6 (v6.10.0), pyside6_addons, pyside6_essentials

**Datenverarbeitung**: pandas

Text & Formatierung: markdown, htmlentities

**Visualisierung**: graphviz (wichtig für die Darstellung von Strukturen/Netzplänen)

---

**Installation:**
Repository klonen:

Bash

git clone git@github.com:F-Klose/Verwaltungstool.git
cd Verwaltungstool
Abhängigkeiten installieren:

---

```bash
pip install -r requirements.txt
```

Hinweis: Für die Netzplan-Funktion muss Graphviz zusätzlich auf dem Betriebssystem installiert sein.

---

**Datenverarbeitung & Datenschutz**
Lokale Daten: Personenbezogene Daten (Kalendereinträge, lokale Quiz-Fortschritte) werden ausschließlich lokal in JSON-Dateien gespeichert. Diese sind via .gitignore vom Sync ausgeschlossen.

Geteilte Daten: News, Merksätze und allgemeine Quizfragen werden über GitHub bereitgestellt. Es findet keine Übertragung von Benutzeridentitäten statt.

Sicherheit: Der Passwortgenerator nutzt eine lokale Verschlüsselung; die Sicherheit eingestufter Passwörter ist als "mittel" deklariert (vorgesehen für unkritische Plattformen).

---

**Für Mitarbeitende: Tests & Merges**
Tests ausführen
Bevor Änderungen gepusht werden, sollten die Unittests durchgeführt werden:

Bash

# Alle Tests starten
python -m unittest discover -v

# Spezifische Kalender-Tests
cd attendance_calendar
python -m unittest test_attendance_calendar.py -v
Merge-Konflikte lösen
Sollte es beim git pull zu Konflikten kommen:

Status prüfen: git status

Konflikte in den Dateien manuell lösen oder Versionen vergleichen: git show :2:datei.py (eigene) vs. git show :3:datei.py (andere).


Nach der Lösung: git add . und git commit.

---

Lizenz
MIT-Lizenz: Das Tool selbst steht unter der MIT-Lizenz.

Komponenten: Python und PySide6 unterliegen ihren eigenen jeweiligen Lizenzen.