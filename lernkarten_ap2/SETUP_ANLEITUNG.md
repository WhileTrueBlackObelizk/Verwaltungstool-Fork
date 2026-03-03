# AP2 Lernkarten Quiz - Einrichtung erforderlich

## ⚠️ Quiz ist noch nicht einsatzbereit

Das AP2 Lernkarten Quiz wurde noch nicht kompiliert. Bitte folgen Sie den Schritten unten.

---

## 📋 Schritt-für-Schritt Anleitung

### 1. C# Code kompilieren

Das Quiz-Programm muss zunächst aus C# zu einer Windows-Anwendung (.exe) kompiliert werden.

#### Option A: Mit Visual Studio (empfohlen)
- Öffnen Sie Visual Studio
- Gehen Sie zu: `lernkarten_ap2/main.cs`
- Klicken Sie auf **Build → Release kompilieren**
- Die Datei `main.exe` wird erstellt

#### Option B: Mit Command Line (dotnet)
```bash
cd lernkarten_ap2
dotnet new console --force
dotnet publish -c Release --self-contained true
```

---

### 2. Counter initialisieren

Nach dem Kompilieren müssen die Zählerstände initialisiert werden:

```bash
cd lernkarten_ap2
./main.exe --setup
```

Dies erstellt die Datei `AP2lernkarten_counter.json`.

---

## 📁 Dateistruktur

Nach erfolgreichem Setup sollten folgende Dateien vorhanden sein:

```
lernkarten_ap2/
├── main.exe                      ✓ ERFORDERLICH
├── main.cs                       ✓ vorhanden
├── AP2lernkarten.json           ✓ vorhanden (Fragen)
├── AP2lernkarten_counter.json   ✓ wird erstellt
└── quiz_launcher.py             ✓ vorhanden
```

---

## ✅ Was nach der Einrichtung funktioniert

- **Eine Frage pro Klick** auf den Button
- **Intelligente Fragewahl** - schwierige Fragen häufiger
- **Counter-Verwaltung** - separate Datei ohne Nutzerdaten
- **Kein GitHub-Upload** - Counter-Datei ist in .gitignore

---

## 💡 Tipps

- Die `AP2lernkarten.json` enthält die Fragen und darf angepasst werden
- Die `AP2lernkarten_counter.json` wird automatisch aktualisiert - nicht ändern
- Für neue Fragen: einfach in der JSON-Datei hinzufügen und erneut kompilieren

---

## ❓ Fragen?

Weitere Informationen finden Sie in: `lernkarten_ap2/IMPLEMENTATION.md`

