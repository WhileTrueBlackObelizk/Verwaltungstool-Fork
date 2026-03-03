#----------------------------------------------
# --------------> importe  <-------------------
#----------------------------------------------

import sqlite3
from datetime import datetime, timedelta


#----------------------------------------------
# -------> funktionen der NEWS mit DB <--------
#----------------------------------------------

def get_news(db_path="news/news.db"):
    """
    lädt alle News der letzten 30 Tage aus der SQLite-Datenbank und gibt sie als Liste von Strings zurück.
    Wenn keine News vorhanden sind, wird eine Liste mit dem Eintrag "Keine aktuellen Nachrichten." zurückgegeben.
    30 Tage werden als aktuell betrachtet.
    1. Verbindung zur SQLite-Datenbank herstellen
    2. Alle News abrufen, die in den letzten 30 Tagen erstellt wurden
    3. Verbindung zur Datenbank schließen
    4. Liste der News-Texte zurückgeben oder eine Standardnachricht, wenn keine News vorhanden sind
    5. Die News werden nach Erstellungsdatum absteigend sortiert
    6. Das Datum wird im Format "YYYY-MM-DD HH:MM:SS" gespeichert und verglichen


    
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cutoff_date = datetime.now() - timedelta(days=30)
    cursor.execute(
        "SELECT text, created_at FROM news WHERE datetime(created_at) >= ? ORDER BY datetime(created_at) DESC",
        (cutoff_date.strftime("%Y-%m-%d %H:%M:%S"),)
    )
    news_items = cursor.fetchall()
    conn.close()
    return [row[0] for row in news_items] if news_items else ["Keine aktuellen Nachrichten."]

def delete_old_news(db_path="news/news.db"):
    """Löscht News, die älter als 30 Tage sind, aus der SQLite-Datenbank."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cutoff_date = datetime.now() - timedelta(days=30)
    cursor.execute(
        "DELETE FROM news WHERE datetime(created_at) < ?",
        (cutoff_date.strftime("%Y-%m-%d %H:%M:%S"),)
    )
    conn.commit()
    conn.close()

def add_news_item(text, db_path="news/news.db", created_at=None):
    """Fügt einen neuen News-Eintrag in die SQLite-Datenbank ein."""
    if not text.strip():
        return False
    if created_at is None:
        created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute ("INSERT INTO news (text, created_at) VALUES (?, ?)", (text.strip(), created_at))
    conn.commit()
    conn.close()
    return True


