import random
import string
from typing import Tuple, Dict, List


def generate_random_task_list(num_tasks: int = None) -> Tuple[Dict, Dict, str]:
    """
    Generiert eine zufällige Vorgangsliste mit sinnvollen Abhängigkeiten.

    Args:
        num_tasks: Anzahl der Vorgänge (2-8). Wenn None, wird zufällig gewählt.

    Returns:
        Tuple aus (tasks_dict, preds_dict, csv_content, num_tasks)
    """
    # neu: max. 8 Vorgänge, um Bildbreite zu begrenzen
    if num_tasks is None:
        num_tasks = random.randint(2, 8)
    else:
        num_tasks = min(8, max(2, num_tasks))
    
    # Vorgänge-Namen: A, B, C, ...
    task_names = [chr(ord('A') + i) for i in range(num_tasks)]
    
    # Task-Beschreibungen (zufällig ki generieierte Beispiele, können angepasst werden)
    descriptions = [
        "Anforderungsanalyse",
        "Design erstellen",
        "Implementierung",
        "Code Review",
        "Unit Tests",
        "Integration Tests",
        "Dokumentation",
        "Deployment vorbereiten",
        "Kundenabnahme",
        "Bugfix",
        "Performance-Optimierung",
        "Sicherheitsprüfung",
        "Konfiguration",
        "Training",
        "Go-Live",
        "Monitoring Setup",
        "Datenmigration",
        "Backup-Strategie",
        "Notfallplan",
        "Nachbetreuung",
    ]
    
    tasks = {}
    preds = {}
    
    # Task A hat keine Vorgänger (Start)
    # Startknkoten A
    tasks['A'] = {
        "beschreibung": random.choice(descriptions),
        # Dauer als ganze Zahl (ehemals float war zu unübersichtlich)
        "dauer": random.randint(1, 50)
    }
    preds['A'] = []
    
    # Für jeden weiteren Task: 2-5 zufällige Vorgänger (aber nur aus bereits defiinierten)
    for i, task_name in enumerate(task_names[1:], start=1):
        # Vorgänger: zufällig aus den bereits definiertten Tasks
        available_preds = task_names[:i]  # Alle Tasks vor diesem
        # BEACHTEN:
        # damit möglichst ein zusammenhängender Plan entsteht
        # Der lettzte Vorgang sollte nicht zwingend
        # von jedem anderen abhängen, sonst entsteht eine kastenartige oderr "Stern"-Struktur.
        if i == len(task_names) - 1:  # Letzter Task
            # Zufällig 1-3 Vorgänger aus den vorherigen auswählen, maximal 3 um Übersicht zu behalten
            max_preds = min(3, len(available_preds))
            num_preds = random.randint(1, max_preds) if max_preds > 0 else 0
            selected_preds = random.sample(available_preds, num_preds) if num_preds > 0 else []
        else:
            # Für alle anderen Vorgänge 1-3 Vorgänger auser A 
            max_preds = min(3, len(available_preds))
            num_preds = random.randint(1, max_preds) if max_preds > 0 else 0
            selected_preds = random.sample(available_preds, num_preds) if num_preds > 0 else []
        
        preds[task_name] = sorted(selected_preds)  # Sortiert sonst ändert sich die rihenfolgle bei jedem lauf, was die Tests erschwert
        
        tasks[task_name] = {
            "beschreibung": random.choice(descriptions),
            #------------------------------------------
            # VORGANGSDAUERN kann hier angepasst werden
            #------------------------------------------
            # Verwende ganze Zahlen für die Dauer (1-50), um die Übersicht zu verbessern
            "dauer": random.randint(1, 50)
        }
     
    # CSV generieren für die Aufgabenlist dammit sie in der GUI angezeigt werden 
    csv_lines = ["Vorgang;Beschreibung;Dauer;Vorgänger"]
    
    for task_name in task_names:
        dauer = round(tasks[task_name]["dauer"], 1)
        beschreibung = tasks[task_name]["beschreibung"]
        vorgaenger = ", ".join(preds[task_name]) if preds[task_name] else ""
        
        csv_lines.append(f"{task_name};{beschreibung};{dauer};{vorgaenger}")
    
    csv_content = "\n".join(csv_lines)
    
    # sicherstellendass genau ein Endknoten existiert (ein Knoten ohne Nachfolger)
    # dazu bauen Nachfolgermenge und verbinden
    succs = {name: [] for name in task_names}
    for t, plist in preds.items():
        for p in plist:
            succs[p].append(t)
    ends = [n for n, s in succs.items() if not s]
    if len(ends) > 1:
        # wähle zufällig einen Endknoten, anderen füge ihn als Nachfolger hinzu
        primary = random.choice(ends)
        # alle anderen Endknoten sollen einen Nachfolger bekommen:
        for extra in ends:
            if extra == primary:
                continue
            # füge extra als Vorgänger von primary(Endknoten) hinzu
            if extra not in preds.get(primary, []):
                preds[primary].append(extra)
        # danach haben wir nur noch primary ohne Nachfolger und dammit einen eindueutigen Endknoten
    elif len(ends) == 0 and task_names:
        # falls zufälilig kein Endknoten existiert (immer mindestens einer),
        # ist letzten Task als Endknoten
        last = task_names[-1]
        preds.setdefault(last, [])
    print(" def generate_random_task_list: alles ok")
    return tasks, preds, csv_content, num_tasks


def save_csv(csv_content: str, filepath: str):
    """Speichert CSV-Content in Datei.
        für die GUI, damit die Aufgabenbeschreibung angezeigt werden kann
    """
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(csv_content)
        print(" def save_csv: alles ok")

