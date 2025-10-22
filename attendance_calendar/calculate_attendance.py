import json
from datetime import datetime
from collections import Counter

CLASS_JSON_FILE = "meine_anwesenheit.json"

STATUS_OPTIONS = ["Karlsruhe", "Homeoffice", "Urlaub", "Krankheit", "Feiertag"]

def load_attendance_data():
    try:
        with open(CLASS_JSON_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def calculate_monthly_stats(data, year=None, month=None):
    """Berechnet die Anteile pro Status für einen bestimmten Monat."""
    if not data:
        return {}

    # Standard: aktueller Monat
    now = datetime.now()
    year = year or now.year
    month = month or now.month

    monthly_entries = {
        date: status
        for date, status in data.items()
        if datetime.strptime(date, "%Y-%m-%d").year == year
        and datetime.strptime(date, "%Y-%m-%d").month == month
    }

    if not monthly_entries:
        return {}

    counts = Counter(monthly_entries.values())
    total_days = sum(counts.values())

    stats = {
        status: {
            "tage": counts.get(status, 0),
            "quote": round((counts.get(status, 0) / total_days) * 100, 1)
        }
        for status in STATUS_OPTIONS
    }

    return stats

def print_monthly_overview(stats, year=None, month=None):
    """Gibt eine einfache Übersicht in der Konsole aus."""
    if not stats:
        print("Keine Einträge für diesen Monat gefunden.")
        return

    now = datetime.now()
    year = year or now.year
    month = month or now.month

    print(f"\n📅 Anwesenheitsübersicht ({month:02d}/{year})")
    for status, values in stats.items():
        print(f"{status:12}: {values['tage']} Tage ({values['quote']} %)")