import random


def get_quiz():
    """Rückgabe: prompt, antwort, eingabe_typ ('int' oder 'str') für GUI."""
    zahl = random.randint(1, 100)
    bin_zahl = bin(zahl)[2:]
    prompt = f"Wandle diese Binärzahl in eine Dezimalzahl um: {bin_zahl}"
    return prompt, zahl, 'int'
