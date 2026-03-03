# Verwaltungstool

Zentrales Begleittool für unsere Umschulung — Anwesenheit, Quiz, News und mehr in einer Oberfläche.

> Zwei Personen · Python + PySide6 · Datenaustausch via Git

---

## Start

```bash
./start.sh
```

Installiert fehlende Abhängigkeiten automatisch und startet die App.

---

## Module

| Modul | Funktion |
|---|---|
| 📅 Anwesenheit | Kalender mit farbcodierten Status (Präsenz, HO, Urlaub, Krank, Feiertag) |
| 🧠 Quiz | Adaptive Fragen — häufig falsch beantwortete kommen öfter |
| 📰 News | Kurzmitteilungen, laufen nach 30 Tagen ab |
| 💬 Memos | Rotierende Merksätze (45-Sekunden-Takt) |
| ⚠️ Störungszähler | Zählt technische & allgemeine Störungen pro Tag |
| 🔢 Zahlensysteme | Übungen: Binär ↔ Dezimal ↔ Hexadezimal |
| ⚡ Elektrotechnik | Bildaufgaben mit Antworteingabe |
| 🔑 Passwort | Zufallspasswort-Generator |

---

## Voraussetzungen

- Python 3.10+
- macOS oder Linux

Abhängigkeiten werden beim ersten Start via `start.sh` automatisch installiert.
Manuell: `pip install -r requirements.txt`

---

## Tests

```bash
python -m unittest discover -v
```

---

## Sync

Kein Server. Daten werden als SQLite-Dateien per Git push/pull zwischen beiden Nutzern geteilt.
