# CLAUDE.md — AI Assistant Guide for Verwaltungstool

## Project Overview

**Verwaltungstool** is a PySide6 desktop application built for two people doing a retraining program (Umschulungsprogramm). It organises and supports daily training life with tools for attendance tracking, news sharing, quizzes, disruption counting, memos/quotes, number-system exercises, electrical-engineering exercises, and a password generator.

Data is shared between both users via **Git push/pull** — there is no backend server or REST API. All user-facing text and most internal names are in **German**.

---

## Tech Stack

| Layer | Technology |
|---|---|
| Language | Python 3 |
| GUI Framework | PySide6 6.10 (Qt bindings) |
| Data storage | SQLite 3 (stdlib), JSON files |
| Version control / sync | Git (subprocess calls) |
| Tests | Python `unittest` |
| Dependencies | `requirements.txt` (PySide6 only) |

---

## Repository Layout

```
Verwaltungstool/
├── main.py                        # Application entry point & main window
├── start.py                       # DB initialisation template (not deployed)
├── requirements.txt               # Python dependencies
├── README.md                      # User-facing project documentation
│
├── attendance_calendar/           # Attendance tracking + calendar UI
│   ├── date_attendance_main.py    # Calendar widget, colour-coded statuses
│   ├── calculate_attendance.py    # Attendance statistics
│   └── test_attendance_calendar.py# Unit tests (unittest + PySide6)
│
├── counter/                       # Disruption counter
│   ├── counter_main.py            # Counter dialog (PySide6)
│   ├── under_funktions.py         # SQLite counter logic
│   └── git_funktions.py           # Git push/pull for stoerungen.db
│
├── Elekrotechnick/                # Electrical-engineering exercises
│   ├── gui.py                     # Task display & answer checking
│   ├── main.py                    # Task logic & validation
│   ├── nicht_schummeln.json       # Task definitions (PNG references)
│   └── PNG_e.aufgaben/            # Task image files
│
├── news/                          # News/bulletin board
│   ├── news_main.py               # CRUD + 30-day expiry logic
│   ├── DBsetup.py                 # DB initialisation
│   └── news.db                    # SQLite database (gitignored locally, synced via Git)
│
├── password/
│   └── password_main.py           # Random password generator UI
│
├── quiz/                          # Adaptive quiz module
│   ├── quiz_main.py               # Quiz UI, question management
│   ├── quiz_score_manager.py      # Score tracking helpers
│   ├── quiz_app.sqlite            # Questions/answers DB
│   └── quiz_scores.json           # Per-question wrong-answer counts
│
├── quotes/                        # Memos/quotes rotation
│   ├── quotes_main.py             # CRUD + 45-second rotation
│   └── quotes.db                  # SQLite database
│
├── script/                        # Utility scripts
│   ├── counter.py                 # Stand-alone counter helper
│   └── prüfer.py                  # Validator (vacation/holiday calc)
│
├── styles/                        # Internal styling notes
│   └── flask_mit_gerhardt.md
│
├── utils/
│   └── git_utils.py               # Git utility stubs
│
└── zahlensysteme/                 # Number-system conversion exercises
    ├── Zahlensysteme.md
    └── main/
        ├── main.py                # Entry runner
        ├── gui.py                 # GUI wrapper
        └── fuctions/              # Conversion modules
            ├── binaer_zu_dezi.py
            ├── dezi_zu_binaer.py
            ├── dezi_zu_hexadezi.py
            └── hexadezi_zu_dezi.py
```

---

## Running the Application

```bash
# Install dependencies (once)
pip install -r requirements.txt

# Launch
python main.py
```

---

## Running Tests

```bash
# All tests (from repo root)
python -m unittest discover -v

# Attendance tests only
cd attendance_calendar
python -m unittest test_attendance_calendar.py -v
```

Test coverage currently exists only for `attendance_calendar`. When adding new features, add corresponding tests using Python `unittest`.

---

## Data Storage

### SQLite Databases

| File | Module | Key tables |
|---|---|---|
| `news/news.db` | news | `news(id, text, created_at)` |
| `quotes/quotes.db` | quotes | `zitat(id, text)` |
| `quiz_app.sqlite` | quiz | `frage`, `antwort` |
| `stoerungen.db` | counter | `stoerungen(Art_der_störung, value, datum)` |

### JSON Files

| File | Purpose |
|---|---|
| `meine_anwesenheit.json` | Attendance status per calendar day |
| `quiz/quiz_scores.json` | Wrong-answer count per question |

### Database Access Pattern

All database access uses Python's stdlib `sqlite3` directly — no ORM:

```python
conn = sqlite3.connect(db_path)
cursor = conn.cursor()
cursor.execute("SELECT ...", (param,))   # Always use parameterised queries
conn.commit()
conn.close()
```

Paths are hard-coded as module-level constants:

```python
DB_PATH = "quiz_app.sqlite"
SCORES_PATH = os.path.join(os.path.dirname(__file__), "quiz_scores.json")
```

---

## Multi-User Sync via Git

There is no server. Data sharing between the two users works by committing databases and JSON files to Git and pushing/pulling from the remote:

```python
subprocess.run(["git", "-C", db_dir, "pull", "origin", "main"], check=True)
subprocess.run(["git", "-C", db_dir, "add", db_file], check=True)
subprocess.run(["git", "-C", db_dir, "commit", "-m", "Automatisches Update"], check=True)
subprocess.run(["git", "-C", db_dir, "push", "origin", "main"], check=True)
```

Every data-mutating module (news, counter, quotes) wraps writes with a Git push; reads are preceded by a Git pull. `main.py` also runs a 60-second auto-pull timer (currently disabled — see TODO in `main.py:238`).

---

## GUI Conventions (PySide6)

### Layout hierarchy

```
QMainWindow / QDialog
  └── centralWidget (QWidget)
        └── QVBoxLayout / QHBoxLayout
              ├── QLabel / QPushButton / QLineEdit ...
              └── nested layouts
```

### Signal/slot pattern

```python
button.clicked.connect(self.some_method)
```

### Decorative comment blocks

Large comment headers delimit sections throughout the code:

```python
#----------------------------------------------
# -----> Abschnitt Beschreibung <-----------
#----------------------------------------------
```

Preserve this style when editing existing files.

### Feedback to users

Use `QMessageBox` for confirmations and errors, never `print()`.

### Timers

```python
self.timer = QTimer(self)
self.timer.timeout.connect(self.update_method)
self.timer.start(45000)  # milliseconds
```

---

## Naming & Language Conventions

- **German-first**: all UI strings, most function names, and most variable names are German (e.g., `lade_aufgaben`, `benutzer_eingabe`, `QuotesFenster`).
- Classes use PascalCase even when German (`NewsFenster`, `MainWindow`).
- File names use snake_case or camelCase inconsistently — follow the existing style of the module you are editing.
- **Preserved typo**: The string `"algemein"` (should be `"allgemein"`) in the counter module is intentional — it matches stored database values. Do **not** correct it without migrating the DB.

---

## Module-Specific Notes

### attendance_calendar
- Five status values: `Karlsruhe`, `Homeoffice`, `Urlaub`, `Krankheit`, `Feiertag`.
- Attendance is calculated over a fixed 2-year training period.
- Each status maps to a fixed hex colour defined in `STATUS_COLORS`.

### quiz
- Adaptive: questions with the highest wrong-answer count are shown first.
- Multiple-choice questions support 2–4 answers with at least one correct answer.
- Open TODOs: prevent consecutive duplicate questions; show ≥1 alternative after wrong answer; Git automation for quiz DB.

### news
- News items expire automatically after 30 days (soft expiry, not hard delete).
- `DBsetup.py` must be run once to create the database before first use.

### counter
- Tracks two disruption types: `technisch` and `algemein` (see typo note above).
- Each count is keyed by today's date (`datum = date.today()`).

### zahlensysteme
- Each conversion module exports a single `get_quiz()` function that returns `(prompt, answer, input_type)`.

### Elekrotechnick
- Tasks are defined in `nicht_schummeln.json` with references to PNG images in `PNG_e.aufgaben/`.

---

## Known TODOs

| Location | Description |
|---|---|
| `main.py:238` | Re-enable 60-second Git auto-pull timer |
| `main.py:330` | Move helper functions out of main.py into submodules |
| `start.py:6-8` | Create DB tables for Memos, Counter, Quiz at startup |
| `quiz/quiz_main.py:47` | Prevent same question from appearing consecutively |
| `quiz/quiz_main.py:162` | Show ≥1 alternative question after wrong answer |
| `quiz/quiz_main.py:218` | Git automation for quiz database |
| `quiz/quiz_main.py:254` | Git push after saving a new question |
| `script/prüfer.py` | Vacation, holiday, and school-end-date calculations |

---

## Security Notes

- No personal data is stored — news, quotes, and quiz data are shared anonymously.
- Always use parameterised SQLite queries — never string-format user input into SQL.
- Git subprocess calls use `check=True`; wrap in try/except to surface errors without crashing.

---

## Development Workflow

1. Work on a feature branch (`git checkout -b feature/my-feature`).
2. Test locally with `python -m unittest discover -v`.
3. Commit with a clear message describing **what changed and why**.
4. Open a PR against `master`; the two contributors review and merge.
5. After merging, both users pull `master` so their local databases stay in sync.

---

## Branch Convention (AI Assistants)

When working as an AI assistant on this repository, develop on the branch specified in the task description. Branch names follow the pattern:

```
claude/<session-slug>
```

Always push with:

```bash
git push -u origin <branch-name>
```
