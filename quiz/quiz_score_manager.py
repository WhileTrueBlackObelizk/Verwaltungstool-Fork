import json
import os

def lade_json(dateiname):
    if os.path.exists(dateiname):
        with open(dateiname, 'r') as f:
            return json.load(f)
    return {}

def speichere_json(dateiname, daten):
    with open(dateiname, 'w') as f:
        json.dump(daten, f, indent=2)

def aktualisiere_frage(name, frage_id, richtig, dateiname='quiz_scores.json'):
    daten = lade_json(dateiname)
    if name not in daten:
        daten[name] = {}
    if frage_id not in daten[name]:
        daten[name][frage_id] = 0
    if richtig:
        daten[name][frage_id] -= 1
    else:
        daten[name][frage_id] += 1
    speichere_json(dateiname, daten)
    print(f"Aktueller Stand für {name}: {daten[name]}")

if __name__ == "__main__":
    name = input("Name: ")
    frage_id = input("Frage-ID: ")
    antwort = input("Richtig beantwortet? (j/n): ").lower()
    richtig = antwort == 'j'
    aktualisiere_frage(name, frage_id, richtig)
