import random


def get_quiz():
    """Rückgabe: prompt, antwort, eingabe_typ ('int' oder 'str') für GUI."""
    zahl = random.randint(0, 255)
    prompt = f"Wandle diese Dezimalzahl in eine Hexadezimalzahl um: {zahl}"
    answer = hex(zahl)[2:].upper()
    return prompt, answer, 'str'
