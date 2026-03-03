# AP2 Lernkarten Quiz - Implementierungsanleitung

## Überblick

Das Quiz-System besteht aus:
1. **C# Console-Anwendung** (`main.cs`) - Kernlogik, unabhängig lauffähig
2. **Python Launcher** (`quiz_launcher.py`) - Ruft die .exe von Python auf
3. **PyQt6 Integration** (`quiz_gui_integration.py`) - Dialog für die Haupt-GUI

## Dateistruktur

```
lernkarten_ap2/
├── main.cs                           # C# Quiz-Quellcode
├── main.exe                          # Kompilierte Exe (nach Build)
├── AP2lernkarten.json               # Fragen (OHNE Counter!)
├── AP2lernkarten_counter.json       # Counter (separate Datei, .gitignore!)
├── quiz_launcher.py                 # Python-Wrapper zur Exe
└── quiz_gui_integration.py          # PyQt6 Integration
```

## Schritt 1: C# Projekt compilieren

### Option A: Visual Studio
1. Öffne dein C# Projekt in Visual Studio
2. Ersetze den Code in `main.cs`
3. Build → Release
4. Die `main.exe` wird generiert

### Option B: Command Line (dotnet CLI)
```bash
cd lernkarten_ap2
dotnet new console --force
# Ersetze Program.cs mit main.cs
dotnet publish -c Release --self-contained true
```

## Schritt 2: Struktur vorbereiten

### JSON-Struktur aktualisieren

**AP2lernkarten.json** (OHNE Counter):
```json
[
  {
    "Id": 1,
    "Frage": "Was bewirkt das De Morgan Gesetz bei !(A && B)?",
    "Antwort1": "!A || !B",
    "Antwort2": "!A && !B",
    "KorrekteAntwortIndex": 1
  },
  {
    "Id": 2,
    "Frage": "Welche Datenstruktur ist ein Stack?",
    "Antwort1": "LIFO - Last In, First Out",
    "Antwort2": "FIFO - First In, First Out",
    "KorrekteAntwortIndex": 1
  }
]
```

**AP2lernkarten_counter.json** (wird automatisch erstellt):
```json
[
  {
    "Id": 1,
    "AntwortCounter": 5
  },
  {
    "Id": 2,
    "AntwortCounter": 5
  }
]
```

## Schritt 3: .gitignore Update

Damit keine Nutzerdaten auf GitHub landen:

```bash
# In der Workspace-Wurzel .gitignore hinzufügen:
lernkarten_ap2/AP2lernkarten_counter.json
```

## Schritt 4: Aus der PyQt6 GUI aufrufen

### In deiner main.py:

```python
from pathlib import Path
from lernkarten_ap2.quiz_gui_integration import AP2QuizDialog

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # ... andere UI-Elemente ...
        self.create_quiz_button()
    
    def create_quiz_button(self):
        quiz_btn = QPushButton("AP2 Lernkarten Quiz")
        quiz_btn.clicked.connect(self.open_quiz)
        # Füge den Button zu deinem Layout hinzu
    
    def open_quiz(self):
        # Pfad zur Quiz-Exe
        quiz_exe = Path(__file__).parent / "lernkarten_ap2" / "main.exe"
        
        # Dialog öffnen
        dialog = AP2QuizDialog(self, str(quiz_exe))
        dialog.exec()
```

## Schritt 5: Erste Initialisierung

Beim ersten Laufen die Counter initialisieren:

```python
from lernkarten_ap2.quiz_launcher import AP2QuizLauncher

launcher = AP2QuizLauncher("lernkarten_ap2/main.exe")
launcher.initialize_counter()  # Erstellt AP2lernkarten_counter.json
```

## Wie das Quiz funktioniert

### Ablauf:

1. **Frage laden**: C# lädt `AP2lernkarten.json` und `AP2lernkarten_counter.json`
2. **Beste Frage wählen**: Die Frage mit dem höchsten Counter wird angezeigt
   - Hohe Counter = schwierig = häufig falsch
   - Niedrige Counter = leicht = häufig richtig
3. **Antwort verarbeiten**:
   - ✓ Richtig → Counter -1 (wird leichter)
   - ✗ Falsch → Counter +1 (wird schwieriger)
4. **Counter speichern**: Nur Counter-Datei wird aktualisiert

### Counter-Logik:

```
Startwert: 5

Richtige Antwort:  Counter -= 1  (min. 0)
Falsche Antwort:   Counter += 1

Sortierung: Absteigend
→ Höchste Counter zuerst = Fokus auf schwierige Fragen
```

## Command-Line Optionen

```bash
# Eine Frage stellen
main.exe

# Counter-Datei initialisieren
main.exe --setup

# Hilfe anzeigen
main.exe --help
```

## Architektur-Vorteile

✓ **Datenschutz**: Counter getrennt in separater Datei  
✓ **Unabhängigkeit**: Exe läuft standalone, nicht an Python gebunden  
✓ **Einfache Integration**: Python-Wrapper macht Aufruf einfach  
✓ **Erweiterbar**: Neuen Fragen in JSON einfach hinzufügen  
✓ **Git-freundlich**: Counter-Datei in .gitignore  

## Weitere Features (optional)

### Timer/Timeout für Antworten:
```csharp
// In StartQuiz() statt Console.ReadLine():
var result = ConsoleReadLineWithTimeout(10000); // 10 Sekunden
```

### Mehrere Fragen pro Sitzung:
```csharp
for (int i = 0; i < 5; i++)
{
    StartQuiz();
}
```

### Statistiken/Progress:
```csharp
var statistik = alleCounter
    .Where(c => c.AntwortCounter > 5)
    .Count(); // Schwierige Fragen
```

## Troubleshooting

| Problem | Lösung |
|---------|--------|
| main.exe nicht gefunden | Sicherstellen, dass main.cs compiliert wurde |
| JSON-Fehler | JSON-Format mit `--setup` initialisieren |
| Counter-Datei fehlend | `launcher.initialize_counter()` aufrufen |
| Dateierpfade falsch | Sicherstellen, dass relative Pfade korrekt sind |
