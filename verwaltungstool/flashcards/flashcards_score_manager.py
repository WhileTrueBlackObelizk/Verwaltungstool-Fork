#---------------------------------------------------------------------------------------------------------------------------------------------
# importe <--------------------------<--------------------<--------------------------------
#---------------------------------------------------------------------------------------------------------------------------------------------
import json
import os
from verwaltungstool.config import settings

#---------------------------------------------------------------------------------------------------------------------------------------------
# funtionen <--------------------------<--------------------<--------------------------------
#---------------------------------------------------------------------------------------------------------------------------------------------

QUIZ_SCORE_FILE = settings.QUIZ_JSON


def lade_json():
    """Lädt JSON-Daten aus einer Datei."""
    if os.path.exists(QUIZ_SCORE_FILE):
        with open(QUIZ_SCORE_FILE, 'r') as f:
            return json.load(f)
    return {}

def speichere_json(daten):
    """Speichert JSON-Daten in eine Datei."""
    with open(QUIZ_SCORE_FILE, 'w') as f:
        json.dump(daten, f, indent=2)

def aktualisiere_frage(name, frage_id, richtig):
    """Aktualisiert den Punktestand für eine bestimmte Frage eines Benutzers."""
    daten = lade_json(QUIZ_SCORE_FILE)
    if name not in daten:# neuer benutzer
        daten[name] = {}
    if frage_id not in daten[name]:# fragen
        daten[name][frage_id] = 0 # initialer punktestand
    if richtig:
        daten[name][frage_id] -= 1# richtige antwort
    else:
        daten[name][frage_id] += 1# falsche antwort
    speichere_json(QUIZ_SCORE_FILE, daten)
    print(f"Aktueller Stand für {name}: {daten[name]}")

if __name__ == "__main__":
    name = input("Name: ")
    frage_id = input("Frage-ID: ")
    antwort = input("Richtig beantwortet? (j/n): ").lower()
    richtig = antwort == 'j'
    aktualisiere_frage(name, frage_id, richtig)
