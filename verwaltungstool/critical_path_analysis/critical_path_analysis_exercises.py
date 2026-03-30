import sys
import os
import tempfile
from pathlib import Path

from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QTableWidget, QTableWidgetItem, QLabel, QScrollArea
)
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt

from verwaltungstool.critical_path_analysis.critical_path_analysis_core import load_csv, compute_cpm, build_dot, render_dot
from verwaltungstool.critical_path_analysis.critical_path_analysis_generator import generate_random_task_list, save_csv

#------------------------------
#gui
#-------------------------------
class NetzplanUebungWindow(QMainWindow):
    def __init__(self, auto_generate: bool = True):
        super().__init__()
        self.setWindowTitle("Netzplan Übung")
        self.setGeometry(100, 100, 1400, 900)
        
        self.current_csv_path = None
        self.current_tasks = None
        self.current_preds = None
        self.current_metrics = None
        self.current_project_duration = None
        
        self.init_ui()
        # Beim Erstellen eines Fensters für Tests oder spezielle Zwecke
        # kann das automatische Erzeugen einer Aufgabe unterdrückt werden.
        if auto_generate:
            self.generate_new_exercise()
            #print(" def __init__: alles ok")

    
    def init_ui(self):
        """Initialisiert die Benutzeroberfläche."""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QVBoxLayout()
        
        # Titel
        title_label = QLabel("Netzplan Übung")
        title_label.setStyleSheet("font-size: 18px; font-weight: bold;")
        main_layout.addWidget(title_label)
        
        # Container für Aufgabe und Lösung
        self.content_layout = QVBoxLayout()
        main_layout.addLayout(self.content_layout)
        
        # Button-Leiste unten
        button_layout = QHBoxLayout()
        
        self.button_fertig = QPushButton("Fertig")
        self.button_fertig.clicked.connect(self.show_solution)
        button_layout.addWidget(self.button_fertig)
        
        self.button_abbrechen = QPushButton("Abbrechen")
        self.button_abbrechen.clicked.connect(self.cancel_exercise)
        button_layout.addWidget(self.button_abbrechen)
        
        self.button_neue_uebung = QPushButton("Neue Übung")
        self.button_neue_uebung.clicked.connect(self.generate_new_exercise)
        self.button_neue_uebung.setVisible(False)
        button_layout.addWidget(self.button_neue_uebung)
        
        self.button_beenden = QPushButton("Beenden")
        self.button_beenden.clicked.connect(self.close)
        self.button_beenden.setVisible(False)
        button_layout.addWidget(self.button_beenden)
        
        main_layout.addLayout(button_layout)
        central_widget.setLayout(main_layout)
        #print(" def init_ui: alles ok")

    
    def clear_content(self):
        """Leert den Content-Bereich."""
        while self.content_layout.count():
            widget = self.content_layout.takeAt(0).widget()
            if widget:
                widget.deleteLater()
                #print(" def clear_content: alles ok")

    
    def generate_new_exercise(self):
        """Generiert eine neue zufällige Übungsaufgabe."""
        self.clear_content()
        
        # Neue Aufgabe generieren
        self.current_tasks, self.current_preds, csv_content, num_tasks = generate_random_task_list()
        
        # Temporary CSV-Datei erstellen
        self.current_csv_path = os.path.join(tempfile.gettempdir(), "netzplan_aufgabe.csv")
        save_csv(csv_content, self.current_csv_path)
        
        # Buttons konfigurieren
        self.button_fertig.setVisible(True)
        self.button_abbrechen.setVisible(True)
        self.button_neue_uebung.setVisible(False)
        self.button_beenden.setVisible(False)
        
        # Aufgabe anzeigen
        self.show_exercise()
        #print(" def generate_new_exercise: alles ok")

    
    def show_exercise(self):
        """Zeigt die Aufgabe (CSV-Tabelle) an."""
        self.clear_content()
        
        # Titel
        task_label = QLabel(f"Aufgabe: Berechnen Sie den kritischen Pfad")
        task_label.setStyleSheet("font-size: 14px; font-weight: bold; margin: 10px 0;")
        self.content_layout.addWidget(task_label)
        
        # CSV in Tabelle anzeigen
        try:
            df = load_csv(self.current_csv_path)[0]  # load_csv gibt (tasks, preds) zurück, wir brauchen nur die Datei
            
            # Neulladen mit Pandas für Table
            import pandas as pd
            df = pd.read_csv(self.current_csv_path, sep=";", dtype=str).fillna("")
            
            table = QTableWidget()
            table.setColumnCount(len(df.columns))
            table.setRowCount(len(df))
            table.setHorizontalHeaderLabels(df.columns)

            
            for row_idx, row in df.iterrows():
                for col_idx, (col_name, value) in enumerate(row.items()):
                    item = QTableWidgetItem(str(value))
                    item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)  # Read-only
                    table.setItem(row_idx, col_idx, item)
            
            table.resizeColumnsToContents()
            self.content_layout.addWidget(table)
        
        except Exception as e:
            error_label = QLabel(f"Fehler beim Laden der CSV: {e}")
            self.content_layout.addWidget(error_label)
        
        # Streetch am Ende fuer bessere Optik
        self.content_layout.addStretch()
        #print(" def show_exercise: alles ok")


    def show_solution(self):
        """Berechnet und zeigt die Lösung an."""
        self.clear_content()
        
        try:
            # CPM berechnen
            self.current_metrics, self.current_project_duration, topo, succs = compute_cpm(
                self.current_tasks, self.current_preds
            )
            
            # DOT generierenn
            dot_content = build_dot(self.current_tasks, self.current_preds, self.current_metrics, self.current_project_duration)
            
            # Temporary DOT-Datei 
            dot_path = os.path.join(tempfile.gettempdir(), "netzplan_solution.dot")
            png_path = os.path.join(tempfile.gettempdir(), "netzplan_solution.png")
            
            with open(dot_path, "w", encoding="utf-8") as f:
                f.write(dot_content)
            
            # PNG rendern
            try:
                render_dot(dot_path, png_path)
            except Exception as e:
                # Graphviz fehlt oder ein anderes Problem trat auf
                error_label = QLabel(f"Fehler beim Rendern der Grafik: {e}")
                error_label.setStyleSheet("color: red;")
                self.content_layout.addWidget(error_label)
                # Simulation der Netzplan-Grafik mit QGraphicsView als Fallback
                # (einfacher Platzhalter, damit die Methode immer existiert)
                try:
                    self.draw_network_graph()
                except AttributeError:
                    # ältere Versionen hatten die Methode nicht definiert;
                    # ein simpler Hinweis hilft dem Benutzer weiter.
                    fallback_label = QLabel(
                        "(Grafik nicht verfügbar; Graphviz fehlt oder konnte nicht ausgeführt werden.)"
                    )
                    fallback_label.setStyleSheet("color: gray; font-style: italic;")
                    self.content_layout.addWidget(fallback_label)
                # Ergebnis-Tabelle anzeigen
                self.show_results_table()
                # Buton-Status beibehalten wie bei fertiger Lösung
                self.button_fertig.setVisible(False)
                self.button_abbrechen.setVisible(False)
                self.button_neue_uebung.setVisible(True)
                self.button_beenden.setVisible(True)
                self.content_layout.addStretch()
                return
            
            # Tittel
            solution_label = QLabel("Lösung: Kritischer Pfad (rot markiert)")
            solution_label.setStyleSheet("font-size: 14px; font-weight: bold; margin: 10px 0;")
            self.content_layout.addWidget(solution_label)
            
            # PNG Aanzeige
            pixmap = QPixmap(png_path)
            if not pixmap.isNull():
                img_label = QLabel()
                # begrenze die Breite des Bildes etwas, damit es nicht zu groß wird
                max_width = 800
                # scaledToWidth akzeptiert als zweiten Parameter nur den
                # Transformationsmodus; die Beibehaltung des Seitenverhältnisses
                # ist standardmäßig aktiviert.
                img_label.setPixmap(pixmap.scaledToWidth(max_width, Qt.SmoothTransformation))
                
                scroll = QScrollArea()
                scroll.setWidget(img_label)
                scroll.setWidgetResizable(True)
                self.content_layout.addWidget(scroll)
            else:
                error_label = QLabel("Fehler beim Rendern der Grafik")
                self.content_layout.addWidget(error_label)
            
            # Ergebnis-Tabellle anzeigen
            self.show_results_table()
            
        except Exception as e:
            error_label = QLabel(f"Fehler bei der Berechnung: {e}")
            error_label.setStyleSheet("color: red;")
            self.content_layout.addWidget(error_label)
        
        # Buttons für Löoesung anzeigen
        self.button_fertig.setVisible(False)
        self.button_abbrechen.setVisible(False)
        self.button_neue_uebung.setVisible(True)
        self.button_beenden.setVisible(True)
        
        # am Ende
        self.content_layout.addStretch()# stretch= heist das der restliche plat flexibel bleibt und die Elemente oben bleiben
        #print(" def show_solution: alles ok")

    def show_results_table(self):
        """Zeigt die berechneten CPM-Werte in einer Tabelle."""
        if not self.current_metrics:
            return
        
        results_label = QLabel("Berechnete Werte (FAZ, FEZ, SAZ, SEZ, GP, FP):")
        results_label.setStyleSheet("font-size: 12px; font-weight: bold; margin-top: 20px;")
        self.content_layout.addWidget(results_label)
        
        # Ergebnis-Tabelle mit werten 
        results_table = QTableWidget()
        results_table.setColumnCount(7)
        results_table.setHorizontalHeaderLabels(["Vorgang", "FAZ", "FEZ", "SAZ", "SEZ", "GP", "FP"])
        results_table.setRowCount(len(self.current_metrics))
        
        # Kritische Vorgänge markieren (kritischer pfad ohne Pufferzeit)
        critical_tasks = {n for n, m in self.current_metrics.items() if abs(m["GP"]) < 1e-9}
        
        for row_idx, (task_name, metrics) in enumerate(sorted(self.current_metrics.items())):
            items = [
                QTableWidgetItem(task_name),
                QTableWidgetItem(f"{metrics['FAZ']:.1f}"),
                QTableWidgetItem(f"{metrics['FEZ']:.1f}"),
                QTableWidgetItem(f"{metrics['SAZ']:.1f}"),
                QTableWidgetItem(f"{metrics['SEZ']:.1f}"),
                QTableWidgetItem(f"{metrics['GP']:.1f}"),
                QTableWidgetItem(f"{metrics['FP']:.1f}"),
            ]
            
            for col_idx, item in enumerate(items):
                item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)  # Read-only
                
                # Kritische Vorgänge rot markieren zurr besserreb uebersicht
                if task_name in critical_tasks and col_idx == 0:
                    item.setBackground(Qt.GlobalColor.red)
                
                results_table.setItem(row_idx, col_idx, item)
        
        results_table.resizeColumnsToContents()
        self.content_layout.addWidget(results_table)
        
        # Projektdauergesammt anzeigen
        duration_label = QLabel(f"Projekt-Dauer: {self.current_project_duration:.1f} Tage")
        duration_label.setStyleSheet("font-size: 11px; color: #333; margin-top: 10px;")
        self.content_layout.addWidget(duration_label)
        #print(" def show_results_table: alles ok")


    def cancel_exercise(self):
        """Bricht die aktuelle Übung ab."""
        self.generate_new_exercise()
        #print(" def cancel_exercise: alles ok")

    # ------------------------------------------------------------------
    # Fallback-Zeichnung
    # ------------------------------------------------------------------
    def draw_network_graph(self):
        """Zeichnet einen einfachen Hinweis, wenn Ggraphviz nicht verfügbar ist.
        """

        notice = QLabel(
            "Graphische Darstellung nicht verfügbar (Graphviz nicht installiert)."
        )
        notice.setStyleSheet("color: gray; font-style: italic;")
        self.content_layout.addWidget(notice)
        #print(" def draw_network_graph: alles ok")

#---------------------------------
# Hauptfunktion zum Starten der GUI
#---------------------------------

def main():
    """ 
    hier wird die GUI gestartet, damit die Übungsaufgaben angezeigt werden können
    """
    app = QApplication(sys.argv)
    window = NetzplanUebungWindow()
    window.show()
    sys.exit(app.exec())
    #print(" def main: alles ok")


if __name__ == "__main__":
    main()
