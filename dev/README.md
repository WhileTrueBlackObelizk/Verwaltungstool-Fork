# Development Tools

Hilfsskripte und Utilities zur Entwicklung und zum Debugging des Verwaltungstools.

## Scripts

### `check_dependencies.py`
Überprüft die Installation aller erforderlichen Python-Pakete und externen Binaries.

**Verwendung:**
```bash
python dev/check_dependencies.py
```

**Was wird geprüft:**
- Python-Version und Ausführbarer Pfad
- Installierte Python-Pakete:
  - PySide6 (GUI-Framework)
  - htmlentities (HTML-Entity-Verarbeitung)
  - pandas (Datenverarbeitung)
  - markdown (Markdown-Rendering)
- Externe Binaries:
  - Graphviz `dot` (für Netzplan-Generierung)

**Beispiel-Ausgabe:**
```
✓ PySide6               6.10.0                 GUI-Framework
✓ htmlentities         1.3.0                  HTML-Entity-Verarbeitung (Netzplan)
✗ graphviz             nicht gefunden         nicht installiert
```

Wenn Fehler erkannt werden, zeigt das Skript hilfreiche Installationsbefehle.

## Hinzufügen neuer Dev-Tools

1. Neues Python-Skript im `dev/`-Ordner erstellen
2. Dokumentation in dieser `README.md` hinzufügen
3. Optional: Beschreibung in `__init__.py` ergänzen
