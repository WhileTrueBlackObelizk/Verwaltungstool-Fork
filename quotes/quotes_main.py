import sqlite3
import subprocess




def get_quotes(db_path="quotes/quotes.db"):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute ("SELECT text FROM Zitat")
    quotes = cursor.fetchall()
    conn.close()
    return [row[0] for row in quotes] if quotes else ["Keine Zitate."]

def add_quotes(text, db_path="quotes/quotes.db"):
    if not text.strip():
        return False
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute ("INSERT INTO Zitat (text) VALUES (?)", (text.strip(),))
    conn.commit()
    conn.close()
    return True

def git_pull_quotesdb():
    """Holt die aktuelle quotes.db von Git."""
    try:
        subprocess.run(["git", "pull"], check=True)
        print("Git Pull für quotes.db ausgeführt.")
    except Exception as e:
        print(f"Fehler bei git pull: {e}")

def git_push_quotesdb(commit_message="Update quotes.db"):
    """Pusht die aktuelle quotes.db zu Git."""
    try:
        subprocess.run(["git", "add", "quotes.db"], check=True)
        subprocess.run(["git", "commit", "-m", commit_message], check=True)
        subprocess.run(["git", "push"], check=True)
        print("Git Push für quotes.db ausgeführt.")
    except Exception as e:
        print(f"Fehler bei git push: {e}")

def git_merge_quotesdb():
    """Führt ein git merge aus (z.B. nach Pull)."""
    try:
        subprocess.run(["git", "merge"], check=True)
        print("Git Merge für quotes.db ausgeführt.")
    except Exception as e:
        print(f"Fehler bei git merge: {e}")


