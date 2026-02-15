---
marp = True
---
# Verwaltungstool

Dieses Verwaltungstool wurde entwickelt, um sämtliche organisatorische Aufgaben während unserer Umschulung effizient und übersichtlich zu gestalten. Ziel ist es, alle bisher genutzten Einzeltools in einer zentralen Anwendung zusammenzuführen und sowohl Verwaltungs- als auch Hilfsfunktionen bereitzustellen.

**Teamgröße:** 2 Personen

---

## Funktionsübersicht

### Verwaltungstools
- **Tagesberichte:** Automatisierte Erstellung von Tagesberichten als Textdateien mit spezifischer Benennung.
- **Berichtszählung & Kategorisierung:** Übersichtliche Einteilung der Berichte in Kategorien wie Präsenz, Homeoffice, Krank, Urlaub und Sonderfälle.
- **Duplikatkontrolle:** Sicherstellung, dass keine Tagesberichte doppelt angelegt werden.

---

### Hilfstools
- **Quiz:** Zufällige Lerneinheiten mit 2–4 Antwortmöglichkeiten, Auswertung und Lernfortschritts-Tracking.
- **Störungscounter:** Sammlung und Auswertung technischer und allgemeiner Störungen (wird von allen Anwendern geteilt, keine personenbezogenen Daten).
- **News:** Kurzmitteilungen, die für 2 Wochen sichtbar bleiben und automatisiert über GitHub verteilt werden.
- **Merksätze:** Rotierende Anzeige von Merksätzen, die alle 120 Sekunden wechseln.
- **Zahlensysteme:** Ermoeglicht ueben der umrechnungen zwischen den einzelnen zahlen systemen (Binaer/Hexadezimal/Dezimal)

- **Passwort generrator**
erstellt passwörter mit random zeichen auf angebene länge 
---

## Technische Umsetzung

- **Programmiersprache:** Python
- **GUI:** PySide6
- **Hauptfenster:** Die zentrale Steuerung erfolgt über die Datei `Main.py`.
- **Datenschutz:** Es werden keine personenbezogenen Daten verarbeitet. Alle geteilten Inhalte (News, Merksätze, Quizfragen) sind anonymisiert.

---

## GitHub & Versionsverwaltung

- **Datenverteilung:** News, Merksätze und Quizfragen werden über GitHub bereitgestellt, ohne Speicherung von Benutzerdaten.

---

## Lizenz

- **MIT-Lizenz:** Kompatibel mit Python und PySide6. Bei Weiterverwendung ist eine Erwähnung erforderlich.
- **PySide6 & Python:** Beide Komponenten unterliegen eigenen Lizenzen.

---

## Kalenderfunktion

Der integrierte Kalender erstellt ein Raster basierend auf dem aktuellen Datum. Jeder Tag ist als anklickbare Box dargestellt und bietet folgende Optionen:
- **Tagesbericht erstellen:** Vier Varianten, z.B. `2025_09_22_tagesbericht_K`

---

- **Steuerungsmenü (oben):**
  - Vorheriger Monat
  - Nächster Monat
  - Prüfungsfunktion (Duplikate erkennen, Listenabgleich)
  - Zählfunktion (prozentuale Übersicht vorhandener Berichte)

---

- **Menü (unten):**
  - Zurück-Button
  - Button zum Festlegen des Speicherverzeichnisses für Tagesberichte
  - Umschalten des Kalenderlayouts (KW-/Monatsansicht)

---

## Passwortgenerator

Der integrierte Passwortgenerator ermöglicht die Erstellung sicherer Passwörter mit frei wählbarer Länge. Passwörter werden verschlüsselt lokal gespeichert. Für die Entschlüsselung ist ein Master-Passwort erforderlich.

---

## Prüfer und Zähler

Für die effiziente Verwaltung und Kontrolle der Tagesberichte stehen zwei eigenständige Python-Skripte zur Verfügung:

- **Zähler:** Dieses Skript ermöglicht die automatische Ermittlung der Anzahl vorhandener Tagesberichte. So kann jederzeit nachvollzogen werden, wie viele Berichte bereits erstellt wurden und wie hoch der aktuelle Erfüllungsgrad (Prozentsatz) ist.
- **Prüfer:** Mit diesem Skript lassen sich Tagesberichte auf Duplikate und fehlende Einträge überprüfen. Dadurch wird sichergestellt, dass keine doppelten Berichte existieren und keine Berichte fehlen. Die Ergebnisse können direkt mit den Anwesenheitslisten der Dozenten abgeglichen werden.

Diese Werkzeuge unterstützen eine schnelle und zuverlässige Kontrolle der Anwesenheit und Berichterstattung und helfen dabei, die eigenen Planungen optimal anzupassen.


---

## Zielsetzung

Mit diesem Tool schaffen wir eine zentrale, datenschutzkonforme und benutzerfreundliche Lösung für alle relevanten Verwaltungs- und Lernprozesse während unserer Umschulung. Die modulare Struktur ermöglicht eine einfache Erweiterung und Anpassung an zukünftige Anforderungen.

---

## Für Mitarbeitende: Lokal testen und Merge-Checks (Deutsch)

Dieser Abschnitt beschreibt kurz und knapp, wie Mitwirkende das Projekt lokal testen und typische Merge-Probleme prüfen und lösen können.

Voraussetzungen
- macOS oder Linux mit Python 3.10+ installiert (macOS-Anwender: zsh ist Standard)
- Optional: ein virtuelles Umfeld (venv) zur Isolierung von Abhängigkeiten

Schnellstart (einmalig)
1. Projekt klonen (falls noch nicht vorhanden):

```bash
git clone git@github.com:F-Klose/Verwaltungstool.git
cd Verwaltungstool
```

2. Optional: virtuelles Umfeld erstellen und aktivieren:

```bash
python -m venv .venv
source .venv/bin/activate  # für zsh / bash
```

3. Benötigte Pakete installieren (mindestens PySide6):

```bash
pip install --upgrade pip
pip install PySide6
# Falls weitere Abhängigkeiten hinzugefügt werden, hier ergänzen
```

Tests ausführen
- Alle Tests (aus dem Projekt-Root):

```bash
python -m unittest discover -v
```

- Nur die Tests des Attendance-Modules (aus dem Ordner `attendance_calendar`):

```bash
cd attendance_calendar
python -m unittest test_attendance_calendar.py -v
```

- Wenn das Projekt eine lokale virtuelle Umgebung `.venv` nutzt, können Sie stattdessen explizit den Python-Interpreter verwenden:

```bash
./.venv/bin/python -m unittest discover -v
```

Hinweise zu GUI-Tests
- Die Tests im Ordner `attendance_calendar` verwenden PySide6-Widgets. Stellen Sie sicher, dass PySide6 installiert ist und dass der Testlauf eine QApplication-Instanz erstellt (die Tests in diesem Repo setzen die QApplication automatisch in `setUpClass`).

Merge- und Konflikt-Checks (kurz)
1. Prüfen, ob ein Merge-Konflikt vorliegt:

```bash
git status --porcelain
git diff --name-only --diff-filter=U
```

2. Wenn Dateien ungemerged sind, die Stage-Blobs ansehen (zeigt die Versionen von beiden Seiten):

```bash
git ls-files -u
git show :1:path/to/file.py   # Version von stage 1
git show :2:path/to/file.py   # Version von stage 2
git show :3:path/to/file.py   # Version von stage 3 (falls vorhanden)
```

3. Konflikt auflösen (Beispiel-Workflow):
- Wähle die gewünschte Version, schreibe sie in die Arbeitskopie (z. B. `git show :3:... > file.py`) oder editiere manuell.
- `git add file.py` um die Datei als gelöst zu markieren.
- Sobald alle Konflikte gelöst sind: `git commit -m "Merge: Konflikte gelöst: <kurze Beschreibung>"`
- Danach `git push` zum Remote-Branch.

Best Practices für Tests vor dem Push
- Immer `python -m unittest discover -v` lokal ausführen bevor Sie Änderungen pushen.
- Wenn Sie an GUI- oder Zeit-abhängigen Tests arbeiten, stellen Sie sicher, dass die Tests deterministisch sind (keine festen Zeitlimits in Produktionscode verwenden).

Kontakt / Rückfragen
- Wenn Unsicherheit bei der Konfliktlösung besteht: Eröffnen Sie eine kurze Pull-Request mit dem Merge-Commit und markieren Sie einen Teamkollegen zur Review.
- Bei Problemen mit PySide6-Importen prüfen Sie zuerst die aktive Python-Umgebung (`which python` / `python -V`) und ob PySide6 in dieser Umgebung installiert ist (`pip list | grep PySide6`).

Diese Anleitung ist bewusst knapp gehalten — bei Bedarf erstelle ich gern eine ausführlichere `CONTRIBUTING.md` mit Checklisten und CI-Hinweisen.