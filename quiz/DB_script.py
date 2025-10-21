import sqlite3
import json
import os
import subprocess

#GIT_REPRO_URL = ""
DB_FILENAME = "quiz.db"
#Counter_FILE = "counter.json"
#BRANCH = "main"():
   
#def get_db_file_pull():
 #   subprocess.run(["git", "pull", "origin", BRANCH])
  #  return DB_FILENAME

def create_DB():
    if not os.path.exists(DB_FILENAME):
        conn = sqlite3.connect(DB_FILENAME)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS quiz (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                question TEXT NOT NULL,
                answer TEXT NOT NULL,
                answer2 TEXT NOT NULL,
                answer3 TEXT,
                answer4 TEXT,
                correct_answer INTEGER NOT NULL,
                category TEXT
            )
        ''')
        conn.commit()
        conn.close()
    else:
        print("Database already exists.")

def create_counter_file():
    if not os.path.exists(Counter_FILE):
        with open(Counter_FILE, 'w') as f:
            json.dump({"counter": 0}, f)
    else:
        print("Counter file already exists.") 

create_DB()