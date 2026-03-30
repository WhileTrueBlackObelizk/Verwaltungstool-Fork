import random


def binear_zu_dezimal_quiz():
    """
    EN: Docstring für binear_zu_dezimal_quiz
    here the user is asked to convert a binary number to decimal.
    The user is given a random binary number and must input the decimal equivalent.
    It is then checked whether the input is correct.
    The user receives feedback on whether the input was correct or not.



    DE: Docstring für binear_zu_dezimal_quiz
    hier wird der nutzer gefragt eine binärzahl in dezimal umzuwandeln.
    Der nutzer bekommt eine zufällige binärzahl und muss die dezimalzahl eingeben.
    darauf hin wird überprüft ob die eingabe richtig ist.
    Der Nutzer bekommt eine Rückmeldung ob die Eingabe richtig war oder nicht.
    """

    zahl = random.randint(1, 100)
    bin_zahl = bin(zahl)[2:]
    print(f"wandle diese binärzahl in eine dezimalzahl um: {bin_zahl}")
    try:
        tipp = int(input("ergebnis: "))
        if tipp == zahl:
            print("richtig")
        else:
            print(f"falsch! Die richtige waere: {zahl}")
    except ValueError:
        print("nur zhlen!!!!!!")


def get_quiz():
    """rueckgabe: string, antwort, eingabe_type ('int' oder 'str') fuer GUI."""

    
    zahl = random.randint(1, 100)
    bin_zahl = bin(zahl)[2:]
    prompt = f"wandle diese binärzahl in eine dezimalzahl um: {bin_zahl}"
    return prompt, zahl, 'int'