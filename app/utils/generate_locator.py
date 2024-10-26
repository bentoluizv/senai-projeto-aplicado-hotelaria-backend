import string
from random import choices


def generate_locator():
    letras = ''.join(choices(string.ascii_uppercase, k=2))
    numeros = ''.join(choices(string.digits, k=6))
    return letras + numeros
