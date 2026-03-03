import random


def get_quiz():
    """Rückgabe: prompt, antwort, eingabe_typ ('int' oder 'str') für GUI."""
    zahl = random.randint(1, 100)
    prompt = f"Wandle diese Dezimalzahl in eine Binärzahl um: {zahl}"
    answer = bin(zahl)[2:]
    return prompt, answer, 'str'
