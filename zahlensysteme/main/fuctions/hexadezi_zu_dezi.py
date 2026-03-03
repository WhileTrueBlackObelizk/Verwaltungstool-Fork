import random


def get_quiz():
    """Rückgabe: prompt, antwort, eingabe_typ ('int' oder 'str') für GUI."""
    zahl = random.randint(0, 255)
    hex_zahl = hex(zahl)[2:].upper()
    prompt = f"Wandle diese Hexadezimalzahl in eine Dezimalzahl um: {hex_zahl}"
    return prompt, zahl, 'int'
