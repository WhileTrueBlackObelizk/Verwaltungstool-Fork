-Namen der Ornder - einheitlich umbennenen
-ordnerstruktur überlegen für übersichtlichkeit
-Code in ENG-Sprache



xElektrotechnik -> "electrical_engineering"
Netzplantechnik -> "critical_path_analysis"
Lernkarten -> "flashcards"
Zahlensysteme -> "number systems"
no_cheating


# SF
-Dokus für Funktionen im attendance_calendar
-verschiedene Main.py ümbenennen zur übersicht
-/Elekrotechnick/read_me:E.technick.md umbennenen
-Setup-Datei anlegen die über alle ordner hinweg das setup übernimmt 
-/zahlensysteme/main/main.py übersichtlicher gestalten
-Licensetxt überarbeiten - wegen supabase
-start.py zur allgemeinen setupdatei integrieren 
-db.dateien mit supabase integrieren

-my_project/
├── main.py
├── utils.py
├── models.py
├── services.py
├── test_main.py
├── requirements.txt
└── README.md

# FK
x-styles/md datei könnte weg
-styles/ hier neuen ordener für assets darein dann icon.png
x-counter/löschmich.py löschen
-counter/ git_funktions.py und db nach umstellung entfernen 
-password/ hat noch keine readme
-quiz/ doppel DB
x-quiz/ DB_script.py wird nach umstellung auf supabase unnoetig
-quotes/ DB loeschen da schon übertragen 
x-quotes/ DB erstellungs script kann weg
x-Script/ altlast
-Projekt/ readme akttualiseren in PDF 
-verwaltungstool/ DB´s aufraeumen 
-Verwaltungstool/unterordner/ readme tittel anpassung 
-bennenungen im gesammten projekt standatisieren 
-im gesammten projekt sind __pycache__ datein 
-utils/ wird nach umstellung auf supabase unnoetig
-news/DB nach umstellung DB koennte 
x-start.py veraltet 








# GA


[x] obsolete Dateien löschen 
[x] verwaltungstool-Verzeichnis anlegen
[x] alles bis auf .gitignore, .venv, .vscode, requirements.txt und Readmes erstmal in den verwaltungstool-Ordner verschieben

[X] data-Verzeichnis anlegen (2 Unterverzeichnisse, sqlite und json)

[ ] in allen packages __init__.py anlegen
[X] alle imports anpassen (falls nötig)


[X] Datenbanken in data/sqlite-Ordner verschieben
[X] json-Dateien in data/json-Ordner verschieben
[X] **alle** Dateipfade anpassen/normalisieren

[x] zentrale config-Datei anlegen
[x] zentrale pyproject.toml anlegen
[ ] .env anlegen (gitignore!)

[X] Entscheidung zu supabase/lokal treffen (bleibt beides?)


[ ] supabase-Anbindung aus experimental-Branch picken
[ ] supabase-Anbindung dokumentieren
[ ] json-Speicher-Mechanik auf datenbanken umstellen

[ ] security-Features in supabase reaktivieren