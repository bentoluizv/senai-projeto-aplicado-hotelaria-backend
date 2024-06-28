import random
import string


def generate_locator():
    caracteres = ''.join(random.choices(string.ascii_uppercase, k=2))

    numeros = ''.join(random.choices(string.digits, k=6))

    numero_localizador = caracteres + numeros
    return numero_localizador
