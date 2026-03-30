
import random


def dezimal_zu_binear_quiz():
    """
   EN Docstring für dezimal_zu_binear_quiz
    here the user is asked to convert a decimal number to binary.
    The user is given a random decimal number and must input the binary equivalent.
    It is then checked whether the input is correct.
    The user receives feedback on whether the input was correct or not.

    DE: Docstring für dezimal_zu_binear_quiz
    hier wird der nutzer gefragt eine dezimalzahl in binär umzuwandeln.
    Der nutzer bekommt eine zufällige dezimalzahl und muss die binärzahl eingeben.
    darauf hin wird überprüft ob die eingabe richtig ist.
    Der Nutzer bekommt eine Rückmeldung ob die Eingabe richtig war oder nicht.
    """


    zahl = random.randint(1, 100)
    print(f"wandle diese dezimalzahl in eine binaerzahl um: {zahl}")
    tipp = input("ergebniss: ")
    if tipp == bin(zahl)[2:]:
        print("richtig")
    else:
        print(f"falsch! Die richtige waere: {bin(zahl)[2:]}")


def get_quiz():
    """rueckgabe: string, antwort, eingabe_type ('int' oder 'str') fuer GUI."""

    zahl = random.randint(1, 100)
    prompt = f"wandle diese dezimalzahl in eine binaerzahl um: {zahl}"
    answer = bin(zahl)[2:]
    return prompt, answer, 'str'