import random


def dezimal_zu_hexa_quiz():
    """
    Docstring für dezimal_zu_hexa_quiz
    EN: Here the user is asked to convert a decimal number to hexadecimal.
    The user is given a random decimal number and must input the hexadecimal equivalent.
    It is then checked whether the input is correct.
    The user receives feedback on whether the input was correct or not.

    DE: Hier wird der Nutzer gefragt eine Dezimalzahl in Hexadezimal umzuwandeln.
    Der Nutzer bekommt eine zufällige Dezimalzahl und muss die Hexadezimalzahl
    eingeben. Daraufhin wird überprüft, ob die Eingabe richtig ist.
    Der Nutzer bekommt eine Rückmeldung, ob die Eingabe richtig war oder nicht. 
    """
    zahl = random.randint(0, 255)
    print(f"wandle diese dezimalzahl in eine hexadezmalzahl um: {zahl}")
    tipp = input("ergebniss: ").upper()
    if tipp == hex(zahl)[2:].upper():
        print("richtig")
    else:
        print(f"falsch! Die richtige waere: {hex(zahl)[2:].upper()}")


def get_quiz():
    """rueckgabe: string, antwort, eingabe_type ('int' oder 'str') fuer GUI."""

    zahl = random.randint(0, 255)
    prompt = f"wandle diese dezimalzahl in eine hexadezmalzahl um: {zahl}"
    answer = hex(zahl)[2:].upper()
    return prompt, answer, 'str'