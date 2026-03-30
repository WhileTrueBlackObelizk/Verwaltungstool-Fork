import os
import shutil
import subprocess
import htmlentities
from collections import defaultdict, deque
import csv


# -------------------------
# CSV Parsing
# -------------------------
def parse_predecessors(cell: str):
    """
    DE: hier werden die Vorgänger aus der CSV-Zelle geparst. Es können mehrere Vorgänger durch Komma getrennt angegeben werden.
     - Leere Zelle oder "nan" (case-insensitive) => keine Vorgänger
     - "A, B, C" => ["A", "B", "C"]
     - "A , B" => ["A", "B"] (Trimmen von Leerzeichen)
     - "A,,B" => ["A", "B"] (leere Einträge ignorieren)
  
    EN:  here we parse the predecessors from the CSV cell. Multiple predecessors can be separated by commas.
     - Empty cell or "nan" (case-insensitive) => no predecessors
     - "A, B, C" => ["A", "B", "C"]
     - "A , B" => ["A", "B"] (trimming whitespace)
     - "A,,B" => ["A", "B"] (ignoring empty entries
    """
    s = str(cell).strip()
    if s == "" or s.lower() == "nan":
        return []
    print(" def parse_predecessors: alles ok")
    return [p.strip() for p in s.split(",") if p.strip()]


def load_csv(path: str):
    """
   DE: Lädt die Vorgangsdaten aus einer CSV-Datei. Die CSV muss die Spalten "Vorgang", "Beschreibung", "Dauer" und "Vorgänger" enthalten.
    EN:  Loads the task data from a CSV file. The CSV must contain the columns "Vorgang", "Beschreibung", "Dauer",
    """
    required = ["Vorgang", "Beschreibung", "Dauer", "Vorgänger"]
    tasks = {}
    preds = {}

    with open(path, newline="", encoding="utf-8") as csvfile:# csv öffnen und mit DictReader lesen, damit wir die Spaltennamen verwenden können
        reader = csv.DictReader(csvfile, delimiter=";")
        missing = [c for c in required if c not in reader.fieldnames]
        if missing: # Überprüfen, ob alle erforderlichen Spalten vorhanden sind
            raise ValueError(f"CSV fehlt Spalten: {missing}. Erwartet: {required}")
        for row in reader:  # jede Zeile als dict mit Spaltennamen als keys
            name = row.get("Vorgang", "").strip()
            if not name: # Vorgang ist Pflichtfeld, überspringen wenn leer
                continue
            beschreibung = row.get("Beschreibung", "").strip()
            dauer_str = row.get("Dauer", "").strip().replace(",", ".")
            try: # Dauer in float umwandeln, falls ungültig oder leer => 0.0
                dauer = float(dauer_str) if dauer_str != "" else 0.0
            except ValueError:
                dauer = 0.0 # ungültige Dauer wird als 0 interprertiert
            vorg = row.get("Vorgänger", "")
            vorg_list = parse_predecessors(vorg)
            tasks[name] = {"beschreibung": beschreibung, "dauer": dauer}
            preds[name] = vorg_list

    ids = set(tasks.keys())# Überprüfen, ob alle Vorgänger auch als Vorgang existieren
    for t, plist in preds.items(): # jede Vorgang und seine Vorgänger durchgehen
        bad = [p for p in plist if p not in ids]
        if bad:
            raise ValueError(f"Unbekannte Vorgänger bei {t}: {bad} (kommen nicht als Vorgang vor)")
    return tasks, preds


# -------------------------
# Vorwärts/Rückwärts, Puffer, Kritischer Pfad
# -------------------------
def compute_cpm(tasks, preds):
    """
    DE: Berechnet die CPM-Metriken (FAZ, FEZ, SAZ, SEZ, GP, FP) für die Vorgänge im Netzplan.
     - FAZ: Frühester Anfangszeitpunkt
     - FEZ: Frühester Endzeitpunkt
     - SAZ: Spätester Anfangszeitpunkt
     - SEZ: Spätester Endzeitpunkt
     - GP: Gesamtpuffer (Total Float)
     - FP: Freier Puffer (Free Float)
    EN:  Computes the CPM metrics (FAZ, FEZ, SAZ, SEZ, GP, FP) for the tasks in the network plan.
     - FAZ: Earliest Start Time
     - FEZ: Earliest Finish Time
     - SAZ: Latest Start Time
     - SEZ: Latest Finish Time
     - GP: Total Float
     - FP: Free Float
    """
    ids = list(tasks.keys())# Dauer als float extrahieren, falls sie als String vorliegt (z.B. aus CSV)
    duration = {i: float(tasks[i]["dauer"]) for i in ids}

    succs = defaultdict(list)# Nachfolger bestimmen (für rück und kritischen Pfad)
    indeg = {i: 0 for i in ids}

    for t in ids: # jede Vorgang und seine Vorgänger durchgehen
        for p in preds.get(t, []):
            succs[p].append(t)
            indeg[t] += 1

    q = deque([i for i in ids if indeg[i] == 0]) # Startknoten (Vorgänge ohne Vorgänger) in die Queue für Topo-Sortierung einfügen
    topo = [] # Topologische Sortierung der Vorgänge (Kahn's Algorithmus )
    while q:
        n = q.popleft()
        topo.append(n)
        for s in succs[n]:
            indeg[s] -= 1
            if indeg[s] == 0:
                q.append(s)

    if len(topo) != len(ids):
        raise ValueError("Zyklus erkannt: Netzplan ist nicht azyklisch (DAG). CPM geht so nicht.")

    # vorwärts 
    FAZ, FEZ = {}, {}
    for n in topo:
        if not preds.get(n):
            FAZ[n] = 0.0
        else:
            FAZ[n] = max(FEZ[p] for p in preds[n])
        FEZ[n] = FAZ[n] + duration[n]

    project_duration = max(FEZ.values()) if FEZ else 0.0

    # rückwärts
    SAZ, SEZ = {}, {}
    for n in reversed(topo):
        if not succs[n]:  # Endknoten
            SEZ[n] = project_duration
        else:
            SEZ[n] = min(SAZ[s] for s in succs[n])
        SAZ[n] = SEZ[n] - duration[n]

    # um die Puffer zu berechnen, brauchen wir die Nachfolger-Listen (succs) und die Projekt-Dauer
    GP, FP = {}, {}
    for n in ids:
        GP[n] = SAZ[n] - FAZ[n]  # Gesamtpuffer (Total Float)
        if succs[n]:
            FP[n] = min(FAZ[s] for s in succs[n]) - FEZ[n]  # Freier Puffer
        else:
            FP[n] = project_duration - FEZ[n]

    metrics = {
        n: {"FAZ": FAZ[n], "FEZ": FEZ[n], "SAZ": SAZ[n], "SEZ": SEZ[n], "GP": GP[n], "FP": FP[n]}
        for n in ids
    }
    #print(" def compute_cpm: alles ok")
    return metrics, project_duration, topo, succs


# -------------------------
# bildet die zeichnung für den Netzplan als DOT-String, damit wir sie mit Graphviz rendern können
# -------------------------
def build_dot(tasks, preds, metrics, project_duration):# task: name, beschreibung, dauer; preds: name -> list of vorgänger; metrics: name -> FAZ, FEZ, SAZ, SEZ, GP, FP 
    from collections import defaultdict # import für defalut dict, damit wir die Nachfolger-Listen bauen können

    # Nachfolger bestimmen (fürss "Ende")
    succs = defaultdict(list)
    for t, plist in preds.items():
        for p in plist:
            succs[p].append(t)

    # ggruppierung nach FAZ => gleiche Spalte (rank=same)
    by_es = defaultdict(list)
    for n, m in metrics.items():
        by_es[m["FAZ"]].append(n)

    critical = {n for n, m in metrics.items() if abs(m["GP"]) < 1e-9}
    #print(" def build_dot: alles ok")

    def node_title(name: str) -> str:
        # Visio-Variante zeigt bei Start-/Endknoten gerne "Start zu Ende"
        is_start = len(preds.get(name, [])) == 0
        is_end = len(succs.get(name, [])) == 0
        if is_start and is_end: # wenn ein Vorgang sowohl Start- als auch Endknoten ist (z.B. nur ein Vorgang), dann "Start zu Ende" anzeigen
            return f"Start {name} Ende"
        if is_start: # wenn ein Vorgang nur Startknoten ist, dann "Start {name}" anzeigen
            return f"Start {name}"
        if is_end: # wenn ein Vorgang nur Endknoten ist, dann "{name} Ende" anzeigen
            return f"{name} Ende"
        #print(" def node_title: alles ok")
        return name

    def html_label(name: str) -> str: # um labels zu erstellen( mehrere zeilllen udn spalten)(html-äähnliche labeels zu tabelllen formieren()
        m = metrics[name]
        dur = float(tasks[name]["dauer"])
        title = node_title(name)
        description = htmlentities.encode(tasks[name]["beschreibung"])

        print(" def html_label: vor return alles ok")
        # HTML-like label: 3 Spalten oben, 2. Zeile SAZ/SEZ, unten Titel !!! aufbau !!!
        return f'''<
<TABLE BORDER="1" CELLBORDER="1" CELLSPACING="0" CELLPADDING="4">
  <TR>
    <TD  ALIGN="CENTER">{m["FAZ"]:g}</TD>
    <TD ALIGN="CENTER">&nbsp;</TD>
    <TD ALIGN="CENTER">{m["FEZ"]:g}</TD>
  </TR>

  <TR>
    <TD ALIGN="CENTER"><B>{title}</B></TD>
    <TD ALIGN="CENTER" colspan="2">{description}</TD>
  </TR>

    <TR>
    <TD ALIGN="CENTER">{dur:g}</TD>
    <TD ALIGN="CENTER">{m['GP']:g}</TD>
    <TD ALIGN="CENTER">{m['FP']:g}</TD>
  </TR>

  <TR>
    <TD ALIGN="CENTER">{m["SAZ"]:g}</TD>
    <TD ALIGN="CENTER"></TD>
    <TD ALIGN="CENTER">{m["SEZ"]:g}</TD>
  </TR>

</TABLE>
>'''

    lines = []
    lines.append("digraph Netzplan {")
    lines.append("  rankdir=LR;")
    lines.append("  splines=ortho;")
    lines.append('  graph [fontname="Helvetica", nodesep=0.6, ranksep=0.9];')
    lines.append('  node  [shape=plain, fontname="Helvetica"];')
    lines.append('  edge  [fontname="Helvetica", arrowsize=0.8];')
    lines.append(f'  label="Projekt-Dauer: {project_duration:g}"; labelloc=top; fontsize=18;')

    # Nodes mit HTMLL-Labes erstelen, kritischee Vorgänge ROT einfärben
    for name in tasks.keys():
        label = html_label(name)

        if name in critical:
            lines.append(f'  "{name}" [label={label}, color="red", fontcolor="red", penwidth=4];')
        else:
            lines.append(f'  "{name}" [label={label}];')

    # Ranks (Spalten FAZ)
    for FAZ in sorted(by_es.keys()):
        nodes = " ".join(f'"{n}"' for n in sorted(by_es[FAZ]))
        lines.append(f"  {{ rank=same; {nodes} }}")

    # Kanten erstellen, dabei die Vorgänger-Listen (preds) verwenden
    for t, plist in preds.items():
        for p in plist:
            lines.append(f'  "{p}" -> "{t}";')

    lines.append("}")
    #print(" def html_label: alles ok")
    return "\n".join(lines)
   

# -------------------------
# Hilfsfunktioneen       
# -------------------------

def render_dot(dot_path: str, out_path: str):
    """Rendert die DOT-Datei mit Graphviz """
    dot_exe = shutil.which("dot")
    if not dot_exe:
        raise RuntimeError("Graphviz 'dot' nicht gefunden. Bitte installieren Sie Graphviz.")

    ext = os.path.splitext(out_path)[1].lower().lstrip(".")
    if ext not in ("svg", "png", "pdf"):
        raise ValueError("Output-Endung muss .svg, .png oder .pdf sein")

    subprocess.run([dot_exe, f"-T{ext}", dot_path, "-o", out_path], check=True)
    #print(" def render_dot: alles ok")
    return True
