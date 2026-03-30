
import random


def hexa_zu_dezimal_quiz():
    """EN :
    here the user is asked to convert a hexadecimal number to decimal.
    The user is given a random hexadecimal number and must input the decimal equivalent.
    It is then checked whether the input is correct.
    The user receives feedback on whether the input was correct or not.     

    DE:
    hier wird der nutzer gefragt eine hexadezimalzahl in dezimal umzuwandeln.
    Der nutzer bekommt eine zufällige hexadezimalzahl und muss die dezimalzahl eingeben.
    darauf hin wird überprüft ob die eingabe richtig ist.
    Der Nutzer bekommt eine Rückmeldung ob die Eingabe richtig war oder nicht.  
    
    """
    zahl = random.randint(0, 255)

    hex_zahl = hex(zahl)[2:].upper()
    print(f"wandle diese hexadezmalzahl in eine dezimalzahl um: {hex_zahl}")
    try:
        tipp = int(input("ergebniss: "))
        if tipp == zahl:
            print("richtig")
        else:
            print(f"falsch! Die richtige waere: {zahl}")
    except ValueError:
        print("nur zhlen!!!!!!")


def get_quiz():
    """rueckgabe: string, antwort, eingabe_type ('int' oder 'str') fuer GUI."""

    zahl = random.randint(0, 255)
    hex_zahl = hex(zahl)[2:].upper()
    prompt = f"wandle diese hexadezmalzahl in eine dezimalzahl um: {hex_zahl}"
    return prompt, zahl, 'int'