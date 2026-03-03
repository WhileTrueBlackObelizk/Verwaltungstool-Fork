#---------------------------------------------------------------------------------------------------------------------------------------------
#importe <----------------------------<------------------------------<------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------------------------
import sqlite3
#---------------------------------------------------------------------------------------------------------------------------------------------
# funktionen <----------------------------<------------------------------<--------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------------------------
def get_quotes(db_path="quotes/quotes.db"):
    """Lädt alle Zitate aus der SQLite-Datenbank und gibt sie als Liste von Strings zurück."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute ("SELECT text FROM Zitat")
    quotes = cursor.fetchall()
    conn.close()
    return [row[0] for row in quotes] if quotes else ["Keine Zitate."]

def add_quotes(text, db_path="quotes/quotes.db"):
    """Fügt ein neues Zitat in die SQLite-Datenbank ein."""
    if not text.strip():
        return False
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute ("INSERT INTO Zitat (text) VALUES (?)", (text.strip(),))
    conn.commit()
    conn.close()
    return True


