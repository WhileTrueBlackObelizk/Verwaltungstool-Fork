# logik für Elekrotechnick rechenaufgaben anzeige zur Übung
import json
import os


# Aufgabendaten aus JSON laden
def lade_aufgaben():
    """Lädt die Aufgabendaten aus der nicht_schummeln.json"""
    json_datei = os.path.join(os.path.dirname(__file__), "nicht_schummeln.json")
    try:
        with open(json_datei, "r", encoding="utf-8") as f:
            daten = json.load(f)
            return daten["aufgaben"]
    except FileNotFoundError:
        return []


aufgaben = lade_aufgaben()


def prüfe_antwort(aufgabe_id: int, benutzer_input: str) -> bool:
    """
    Prüft ob der Benutzerinput mit dem korrekten Ergebnis übereinstimmt
    
    Args:
        aufgabe_id: Die ID der Aufgabe
        benutzer_input: Die Eingabe des Benutzers
    
    Returns:
        True wenn korrekt, False wenn falsch
    """
    for aufgabe in aufgaben:
        if aufgabe["id"] == aufgabe_id:
            return benutzer_input.strip() == aufgabe["ergebnis"]
    return False



