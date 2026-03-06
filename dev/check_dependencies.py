#!/usr/bin/env python3
"""
Dependency Checker für das Verwaltungstool
Überprüft die Installation aller erforderlichen Python-Pakete und externen Binaries.

Usage:
    python dev/check_dependencies.py
"""

import sys
import subprocess
import shutil
from pathlib import Path


class Colors:
    """ANSI-Farbcodes für Terminal-Ausgabe."""
    GREEN = "\033[92m"
    RED = "\033[91m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    RESET = "\033[0m"
    BOLD = "\033[1m"


def print_section(title):
    """Gibt einen Abschnittstitel aus."""
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.BLUE}{title}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.RESET}\n")


def check_mark(success):
    """Gibt ein Erfolgs- oder Fehler-Symbol aus."""
    return f"{Colors.GREEN}✓{Colors.RESET}" if success else f"{Colors.RED}✗{Colors.RESET}"


def check_python_package(package_name, import_name=None):
    """
    Überprüft, ob ein Python-Paket installiert ist.
    
    Args:
        package_name: Name des Pakets in pip
        import_name: Name zum Importieren (falls anders als package_name)
    
    Returns:
        tuple: (success: bool, version: str or None)
    """
    """Prüft, ob ein Paket vorhanden ist und liefert seine Version.

    Statt das Modul zu importieren (was beim Laden der großen Bibliothek
    *pandas* auf manchen Anaconda-Systemen wegen numpy-Inkompatibilitäten
    riesige Tracebacks auslöste), benutzen wir `importlib.util.find_spec`
    zur Existenzprüfung und `importlib.metadata` zur Versionsabfrage. Beides
    führt keinen Code im Zielpaket aus.
    """

    import importlib.util
    import importlib.metadata

    import_name = import_name or package_name

    spec = importlib.util.find_spec(import_name)
    if spec is None:
        return False, None

    # Paket ist installierbar; versuche, seine Version zu ermitteln.  Falls
    # es nicht unter dem gleichen Namen registriert ist, geben wir nur einen
    # Platzhalter zurück.
    try:
        version = importlib.metadata.version(package_name)
    except importlib.metadata.PackageNotFoundError:
        version = "unbekannte Version"
    except Exception:
        # Bei ungewöhnlichen Meta-Informationen packen wir die Version
        # ebenfalls nicht aus.
        version = "unbekannte Version"

    return True, version


def check_external_binary(binary_name, common_paths=None):
    """
    Überprüft, ob ein externes Binary (z.B. 'dot') verfügbar ist.
    
    Args:
        binary_name: Name des Binaries (z.B. 'dot')
        common_paths: Liste häufiger Installationspfade
    
    Returns:
        tuple: (found: bool, path: str or None)
    """
    # Versuche über shutil.which (PATH-Suche)
    path = shutil.which(binary_name)
    if path:
        return True, path
    
    # Fallback: Häufige Pfade
    if common_paths:
        for p in common_paths:
            if Path(p).exists():
                return True, p
    
    return False, None


def check_graphviz():
    """Spezielle Überprüfung für Graphviz."""
    graphviz_paths = [
        "/opt/homebrew/bin/dot",      # macOS ARM (Homebrew)
        "/usr/local/bin/dot",          # macOS Intel
        "/usr/bin/dot",                # Linux
        "C:\\Program Files\\Graphviz\\bin\\dot.exe",  # Windows 64-bit
        "C:\\Program Files (x86)\\Graphviz\\bin\\dot.exe",  # Windows 32-bit
    ]
    return check_external_binary("dot", graphviz_paths)


def main():
    """Hauptfunktion."""
    print(f"{Colors.BOLD}{Colors.BLUE}")
    print("╔" + "═"*58 + "╗")
    print("║" + " "*58 + "║")
    print("║" + "Verwaltungstool - Abhängigkeits-Überprüfung".center(58) + "║")
    print("║" + " "*58 + "║")
    print("╚" + "═"*58 + "╝")
    print(Colors.RESET)
    
    # System-Information
    print_section("System-Information")
    print(f"Python-Version: {sys.version}")
    print(f"Python-Ausführbar: {sys.executable}")
    
    # Python-Pakete
    print_section("Python-Abhängigkeiten")
    
    packages = [
        ("PySide6", "PySide6", "GUI-Framework"),
        ("htmlentities", "htmlentities", "HTML-Entity-Verarbeitung (Netzplan)"),
        ("pandas", "pandas", "Datenverarbeitung (Netzplan GUI)"),
        ("markdown", "markdown", "Markdown-zu-HTML-Konvertierung"),
    ]
    
    missing_packages = []
    for package_name, import_name, description in packages:
        success, version = check_python_package(package_name, import_name)
        status = check_mark(success)
        
        if success:
            print(f"{status} {package_name:20} {version:20} {description}")
        else:
            print(f"{status} {package_name:20} {Colors.RED}nicht installiert{Colors.RESET:20} {description}")
            missing_packages.append(package_name)
    
    # Externe Binaries
    print_section("Externe Abhängigkeiten")
    
    # Graphviz / dot
    found, path = check_graphviz()
    status = check_mark(found)
    
    if found:
        print(f"{status} Graphviz 'dot'      {Colors.GREEN}gefunden{Colors.RESET}")
        print(f"   Pfad: {path}")
    else:
        print(f"{status} Graphviz 'dot'      {Colors.RED}nicht gefunden{Colors.RESET}")
        print(f"   Erforderlich für: Netzplan-Rendering")
    
    # Zusammenfassung
    print_section("Zusammenfassung")
    
    if missing_packages:
        print(f"{Colors.RED}Fehlende Python-Pakete:{Colors.RESET}")
        for pkg in missing_packages:
            print(f"  - {pkg}")
        print(f"\n{Colors.YELLOW}Installationsbefehl:{Colors.RESET}")
        print(f"  pip install {' '.join(missing_packages)}")
        print()
    
    if not found:
        print(f"{Colors.RED}Graphviz nicht gefunden.{Colors.RESET}")
        print(f"\n{Colors.YELLOW}Installation:{Colors.RESET}")
        if sys.platform == "darwin":
            print("  macOS (Homebrew): brew install graphviz")
        elif sys.platform.startswith("linux"):
            print("  Linux (Debian/Ubuntu): sudo apt install graphviz")
            print("  Linux (Fedora/RHEL): sudo yum install graphviz")
            print("  Linux (Arch): sudo pacman -S graphviz")
        elif sys.platform == "win32":
            print("  Windows: https://graphviz.org/download/")
        else:
            print("  Siehe: https://graphviz.org/download/")
        print()
    
    # Erfolgs-/Fehlerbericht
    if missing_packages or not found:
        print(f"{Colors.RED}{Colors.BOLD}Status: Einige Abhängigkeiten fehlen!{Colors.RESET}\n")
        return 1
    else:
        print(f"{Colors.GREEN}{Colors.BOLD}Status: Alle Abhängigkeiten sind installiert! ✓{Colors.RESET}\n")
        return 0


if __name__ == "__main__":
    sys.exit(main())
