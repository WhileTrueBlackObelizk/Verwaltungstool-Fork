# logik für Elekrotechnick rechenaufgaben anzeige zur Übung
import json
import random
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
        print(f"Fehler: {json_datei} nicht gefunden!")
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


def rechenaufgabe():
    """
    Zeigt eine zufällige Aufgabe (PNG) an und fragt den Benutzer nach der Lösung.
    Vergleicht die Eingabe mit der korrekten Lösung und gibt Feedback.
    """
    if not aufgaben:
        print("Fehler: Keine Aufgaben geladen!")
        return
    
    # Zufällige Aufgabe auswählen
    aufgabe = random.choice(aufgaben)
    
    print(f"\nAufgabe {aufgabe['id']}: {aufgabe['png']}")
    benutzer_eingabe = input("Gib das Ergebnis ein: ")
    
    # Antwort prüfen
    if benutzer_eingabe.strip() == aufgabe["ergebnis"]:
        print("Richtig!")
    else:
        print("Falsch!")



