# Netzplan-Übungstool

## Übersicht

Das **Netzplan-Übungstool** ist eine interaktive Lernplattform zum Üben und Verstehen von **Projekt-Netzplänen** nach der CPM-Methode (Critical Path Method). Das Tool generiert zufällige Aufgabenlisten und ermöglicht Schülern, den kritischen Pfad selbst zu zeichnen, bevor die automatische Lösung angezeigt wird.

---

## Funktionsweise

### 1. **Aufgabe generieren**
- Das Tool erstellt automatisch eine zufällige Vorgangsliste mit 2–8 Aufgaben (z.B. A, B, C, …).
- Jede Aufgabe hat:
  - **Name**: A, B, C, …
  - **Beschreibung**: z.B. "Anforderungsanalyse", "Design erstellen", …
  - **Dauer**: ganze Zahl in Tagen (z.B. 5, 12, 20, …)
  - **Vorgänger**: von welchen anderen Aufgaben diese abhängt

### 2. **Tabelle anzeigen**
- Die Aufgabendaten werden in einer übersichtlichen **CSV-Tabelle** dargestellt.
- Schüler können diese Tabelle nutzen, um den Netzplan **per Hand zu zeichnen** (auf Papier oder im Tool).
- Tabelle ist schreibgeschützt, um Änderungen zu vermeiden.

### 3. **Lösung berechnen**
- Beim Klick auf **„Fertig"** berechnet das Tool den **kritischen Pfad** mittels CPM:
  - **FAZ** (Frühester Anfangszeitpunkt)
  - **FEZ** (Frühester Endzeitpunkt)
  - **SAZ** (Spätester Anfangszeitpunkt)
  - **SEZ** (Spätester Endzeitpunkt)
  - **GP** (Gesamtpuffer / Total Float)
  - **FP** (Freier Puffer / Free Float)

### 4. **Grafik + Vergleich**
- Das Tool zeigt eine **visuelle Darstellung des Netzplans**:
  - **Knoten** = Vorgänge (mit Name und CPM-Werten)
  - **Kanten** = Abhängigkeiten (Pfeile zwischen Aufgaben)
  - **Kritische Vorgänge** = Rot hervorgehoben (GP = 0)
- Zusätzlich wird eine **Ergebnis-Tabelle** mit allen CPM-Kennzahlen angezeigt.
- Schüler können ihre handgezeichnete Lösung mit der automatischen Lösung vergleichen.

### 5. **Neue Übung**
- Über den Button **„Neue Übung"** können beliebig viele neue Aufgabensätze generiert werden.

---

## Technische Details

### Generator (`critical_path_analysis_generator.py`)
- Erzeugt zufällige Vorgangslisten mit sinnvollen Abhängigkeiten.
- Stellt sicher, dass:
  - Es genau **einen Startknoten** (A) ohne Vorgänger gibt.
  - Es genau **einen Endknoten** ohne Nachfolger gibt.
  - Der Netzplan **zyklenfrei** (DAG) ist.
  - Alle Vorgangsdauern **ganze Zahlen** sind.

### CPM-Berechnung (`critical_path_analysis_core.py`)
- Führt eine **Vorwärtspass**-Berechnung durch (FAZ, FEZ).
- Führt eine **Rückwärtspass**-Berechnung durch (SAZ, SEZ).
- Berechnet **Gesamtpuffer** und **Freien Puffer** für jeden Vorgang.
- Identifiziert den **kritischen Pfad** (Vorgänge mit GP = 0).

### GUI (`critical_path_analysis_exercises.py`)
- Wird über PySide6 (Qt) bereitgestellt.
- Zeigt die Aufgabe in einer **Tabelle** an.
- Beim Klick auf „Fertig":
  - CPM wird berechnet.
  - Netzplan-Grafik wird generiert (mit Graphviz, oder per Fallback).
  - Ergebnis-Tabelle wird angezeigt.
- Unkomplizierte Navigation zwischen neuen Übungen.

---

## Installation & Start

### Voraussetzungen
- **Python 3.8+**
- **PySide6** (für die Benutzeroberfläche)
- (optional) **Graphviz** (`brew install graphviz`) für hochwertige Grafiken

### Start aus dem Hauptmenü
1. Starten Sie die Haupt-Anwendung: `python main.py`
2. Klicken Sie auf den Button **„Netzplan"**.
3. Das Übungsfenster öffnet sich.

### Direkter Start (für Tests)
```bash
cd netzplan_gui_version
python netzplan_uebung.py
```

---

## Beispiel-Ablauf

1. **Aufgabe erscheint:**
   ```
   Vorgang | Beschreibung          | Dauer | Vorgänger
   --------|----------------------|-------|----------
   A       | Anforderungsanalyse  |  5    | 
   B       | Design erstellen     |  7    | A
   C       | Implementierung      | 10    | B
   D       | Testing              |  4    | C
   ```

2. **Schüler zeichnet von Hand einen Netzplan.**

3. **Schüler klickt „Fertig"** → Tool zeigt:
   - **Grafik** des Netzplans mit kritischem Pfad (rot)
   - **Tabelle** mit FAZ, FEZ, SAZ, SEZ, GP für alle Vorgänge
   - **Erkannte Lösung:** Kritischer Pfad = A → B → C → D, Projekddauer = 26 Tage

4. **Schüler vergleicht** seine Zeichnung mit der Lösung.

---

## Didaktischer Wert

- **Aktives Lernen**: Schüler müssen zuerst selbst zeichnen.
- **Sofortiges Feedback**: Automatische Berechnung zeigt richtige Lösung.
- **Beliebig viele Aufgaben**: Generator erzeugt immer neue Fälle.
- **Verständnis stärken**: Werte und kritischer Pfad werden sichtbar.
- **Keine Abhängigkeiten**: Läuft ohne externe Pakete wie Graphviz. 