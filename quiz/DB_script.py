import sqlite3
import json
import os

DB_FILENAME = "quiz_app.sqlite"
SCORES_FILE = "quiz_scores.json"

def create_DB():
    if not os.path.exists(DB_FILENAME):
        conn = sqlite3.connect(DB_FILENAME)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS frage (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                frage_text TEXT NOT NULL,
                quiz_id INTEGER DEFAULT 1
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS antwort (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                antwort_text TEXT NOT NULL,
                frage_id INTEGER NOT NULL,
                ist_richtig INTEGER NOT NULL DEFAULT 0
            )
        ''')
        conn.commit()
        conn.close()
    else:
        print("Database already exists.")

def create_scores_file():
    if not os.path.exists(SCORES_FILE):
        with open(SCORES_FILE, 'w', encoding='utf-8') as f:
            json.dump({}, f, indent=2)
    else:
        print("Scores file already exists.")

create_DB()
create_scores_file()