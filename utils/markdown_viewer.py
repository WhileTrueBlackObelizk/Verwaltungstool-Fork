"""
Markdown Viewer Dialog für die GUI
Zeigt Markdown-Dateien als formatierte HTML an
"""

from PySide6.QtWidgets import QDialog, QVBoxLayout, QTextBrowser, QPushButton, QHBoxLayout
from PySide6.QtCore import Qt
from pathlib import Path
import markdown


class MarkdownViewerDialog(QDialog):
    """Dialog zum Anzeigen von Markdown-Dateien"""
    
    def __init__(self, markdown_file_path: str, title: str = "Information", parent=None):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setGeometry(100, 100, 700, 600)
        self.setModal(True)
        self.init_ui(markdown_file_path)
    
    def init_ui(self, markdown_file_path: str):
        """Initialisiert die UI"""
        layout = QVBoxLayout()
        
        # Text Browser für Markdown
        self.text_browser = QTextBrowser()
        self.text_browser.setMarkdown(self.load_markdown(markdown_file_path))
        layout.addWidget(self.text_browser)
        
        # Close Button
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        close_btn = QPushButton("Schließen")
        close_btn.clicked.connect(self.accept)
        button_layout.addWidget(close_btn)
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
    
    def load_markdown(self, markdown_file_path: str) -> str:
        """
        Lädt eine Markdown-Datei und konvertiert zu HTML
        
        Args:
            markdown_file_path: Pfad zur .md Datei
            
        Returns:
            HTML-String für QTextBrowser
        """
        try:
            file_path = Path(markdown_file_path)
            
            if not file_path.exists():
                return f"""
                <h2>Fehler</h2>
                <p>Datei nicht gefunden: <code>{markdown_file_path}</code></p>
                """
            
            # Markdown laden
            with open(file_path, 'r', encoding='utf-8') as f:
                md_content = f.read()
            
            # Zu HTML konvertieren
            html = markdown.markdown(md_content, extensions=['tables', 'fenced_code'])
            
            # Basis-Styling hinzufügen
            styled_html = f"""
            <html>
            <head>
            <style>
                body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; line-height: 1.6; color: #333; }}
                h1, h2, h3 {{ color: #0366d6; margin-top: 20px; margin-bottom: 10px; }}
                h1 {{ border-bottom: 1px solid #eaecef; padding-bottom: 10px; }}
                code {{ background-color: #f6f8fa; padding: 2px 6px; border-radius: 3px; font-family: monospace; }}
                pre {{ background-color: #f6f8fa; padding: 10px; border-radius: 3px; overflow-x: auto; }}
                blockquote {{ border-left: 4px solid #ddd; margin: 0; padding-left: 16px; color: #666; }}
                table {{ border-collapse: collapse; width: 100%; }}
                table th, table td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
                table th {{ background-color: #f6f8fa; }}
                ul, ol {{ margin-bottom: 10px; }}
                li {{ margin-bottom: 5px; }}
            </style>
            </head>
            <body>
            {html}
            </body>
            </html>
            """
            return styled_html
            
        except Exception as e:
            return f"""
            <h2>Fehler beim Laden der Datei</h2>
            <p>{str(e)}</p>
            """
