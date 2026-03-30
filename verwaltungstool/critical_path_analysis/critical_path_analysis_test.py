"""Unit tests for the Netzplan module.

Die Tests prüfen sowohl die Kernalgorithmen als auch einige Randfälle
wie fehlende Graphviz-Installation.  Das Ziel ist es, sicherzustellen,
dass der Netzplan auf anderen Geräten gebaut werden kann und dass
Fehlerfälle nicht zu Crashs führen (wie es zuvor beim Fallback der Fall
war).
"""

import os
import sys
import tempfile
import unittest

# Damit die Module geladen werden können untersuchen wir denselben
# Importmechanismus wie in ``run.py``: das Verzeichnis des Pakets in
# den Pfad einfügen.
pkg_dir = os.path.join(os.path.dirname(__file__))
sys.path.insert(0, pkg_dir)

from verwaltungstool.critical_path_analysis.critical_path_analysis_core import (
    parse_predecessors,
    load_csv,
    compute_cpm,
    build_dot,
    render_dot,
)
from verwaltungstool.critical_path_analysis.critical_path_analysis_generator import generate_random_task_list

# Für GUI-bezogene Tests wird eine QApplication benötigt.
from PySide6.QtWidgets import QApplication


class TestNetzplanCore(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # QApplication einmal anlegen, falls noch keine existiert.
        cls.app = QApplication.instance()
        if cls.app is None:
            cls.app = QApplication(sys.argv)

    def test_parse_predecessors(self):
        self.assertEqual(parse_predecessors(""), [])
        self.assertEqual(parse_predecessors("nan"), [])
        self.assertEqual(parse_predecessors("A, B ,C"), ["A", "B", "C"])
        self.assertEqual(parse_predecessors("A,,B"), ["A", "B"])

    def test_load_csv_missing_column(self):
        # CSV ohne die erwartete "Vorgänger"-Spalte
        content = "Vorgang;Beschreibung;Dauer\nA;x;1\n"
        with tempfile.NamedTemporaryFile("w", delete=False, suffix=".csv") as f:
            f.write(content)
            path = f.name
        try:
            with self.assertRaises(ValueError):
                load_csv(path)
        finally:
            os.remove(path)

    def test_load_csv_unknown_predecessor(self):
        # Eine Vorgängerbezeichnung, die nicht als Vorgang existiert, soll Fehler
        content = (
            "Vorgang;Beschreibung;Dauer;Vorgänger\n"
            "A;foo;1;B\n"
        )
        with tempfile.NamedTemporaryFile("w", delete=False, suffix=".csv") as f:
            f.write(content)
            path = f.name
        try:
            with self.assertRaises(ValueError):
                load_csv(path)
        finally:
            os.remove(path)

    def test_load_csv_and_compute_cpm(self):
        csv_content = (
            "Vorgang;Beschreibung;Dauer;Vorgänger\n"
            "A;desc;1;\n"
            "B;desc2;2;A\n"
            "C;desc3;3;A, B\n"
        )
        with tempfile.NamedTemporaryFile("w", delete=False, suffix=".csv") as f:
            f.write(csv_content)
            path = f.name

        try:
            tasks, preds = load_csv(path)
            self.assertIn("A", tasks)
            metrics, project_duration, topo, succs = compute_cpm(tasks, preds)
            # Projektende entspricht FEZ des letzten Knotens C
            self.assertEqual(project_duration, metrics["C"]["FEZ"])
            self.assertAlmostEqual(metrics["A"]["FAZ"], 0.0)
        finally:
            os.remove(path)

    def test_compute_cpm_cycle(self):
        # Ein Kreis darf nicht akzeptiert werden
        tasks = {"A": {"dauer": 1}, "B": {"dauer": 1}}
        preds = {"A": ["B"], "B": ["A"]}
        with self.assertRaises(ValueError):
            compute_cpm(tasks, preds)

    def test_build_dot_contains_nodes_and_edges(self):
        tasks = {"A": {"beschreibung": "x", "dauer": 1},
                 "B": {"beschreibung": "y", "dauer": 2}}
        preds = {"A": [], "B": ["A"]}
        metrics, project_duration, topo, succs = compute_cpm(tasks, preds)
        dot = build_dot(tasks, preds, metrics, project_duration)
        self.assertIn('"A" -> "B"', dot)
        self.assertIn('label=', dot)

    def test_render_dot_missing(self):
        # simuliert eine Umgebung ohne dot
        import shutil
        orig = shutil.which
        shutil.which = lambda exe: None
        try:
            with self.assertRaises(RuntimeError):
                render_dot("foo.dot", "foo.png")
        finally:
            shutil.which = orig

    def test_generate_random_task_list(self):
        tasks, preds, csv_content, num = generate_random_task_list(5)
        self.assertEqual(len(tasks), num)
        self.assertIn("A", tasks)
        succs = {name: [] for name in tasks}
        for t, pl in preds.items():
            for p in pl:
                succs[p].append(t)
        ends = [n for n, l in succs.items() if not l]
        self.assertEqual(len(ends), 1)

    def test_draw_network_graph_available(self):
        # lediglich prüfen, dass die Methode existiert und nicht abstürzt
        from verwaltungstool.critical_path_analysis.critical_path_analysis_exercises import NetzplanUebungWindow

        # Erzeuge das Fenster ohne sofortige Aufgabengenerierung, damit
        # keine zusätzlichen Abhängigkeiten (pandas) geladen werden müssen.
        win = NetzplanUebungWindow(auto_generate=False)
        # ersetzen content_layout mit leerem Layout, damit Aufrufe funktionieren
        from PySide6.QtWidgets import QVBoxLayout
        win.content_layout = QVBoxLayout()
        # sollte keinen Fehler werfen
        win.draw_network_graph()


if __name__ == "__main__":
    unittest.main()
