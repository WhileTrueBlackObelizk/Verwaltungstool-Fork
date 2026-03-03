import subprocess
import os

_REPO_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def git_pull():
    """Holt aktuelle Änderungen vom Remote-Repository."""
    try:
        subprocess.run(
            ["git", "-C", _REPO_DIR, "pull", "origin", "master"],
            check=True, capture_output=True
        )
    except subprocess.CalledProcessError as e:
        print(f"Git Pull Fehler: {e.stderr.decode().strip()}")
    except FileNotFoundError:
        print("Git Pull Fehler: git nicht gefunden.")

def git_push():
    """Überträgt lokale Änderungen zum Remote-Repository."""
    try:
        subprocess.run(
            ["git", "-C", _REPO_DIR, "add", "-u"],
            check=True, capture_output=True
        )
        subprocess.run(
            ["git", "-C", _REPO_DIR, "commit", "-m", "Automatisches Update"],
            capture_output=True
        )
        subprocess.run(
            ["git", "-C", _REPO_DIR, "push", "origin", "master"],
            check=True, capture_output=True
        )
    except subprocess.CalledProcessError as e:
        print(f"Git Push Fehler: {e.stderr.decode().strip()}")
    except FileNotFoundError:
        print("Git Push Fehler: git nicht gefunden.")

def git_merge():
    """Führt ausstehende Merges durch."""
    try:
        subprocess.run(
            ["git", "-C", _REPO_DIR, "merge", "--no-edit"],
            check=True, capture_output=True
        )
    except subprocess.CalledProcessError as e:
        print(f"Git Merge Fehler: {e.stderr.decode().strip()}")
    except FileNotFoundError:
        print("Git Merge Fehler: git nicht gefunden.")