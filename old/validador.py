'''validador de contraseña'''


def validar_contrasena(contrasena):
    """Esta funcion valida la contrasena dada como argumento"""

    # condiciones minimas
    longitud_minima = 8
    mayuscula = False
    minuscula = False
    tiene_numero = False
    tiene_caracter_especial = False

    # comprobamos la longitud
    if len(contrasena) < longitud_minima:
        return False

    # caracteres de la contrasena
    for caracter in contrasena:
        if caracter.isupper():
            mayuscula = True

        elif caracter.islower():
            minuscula = True

        elif caracter.isdigit():
            tiene_numero = True

        else:
            tiene_caracter_especial = True
    return mayuscula and minuscula and tiene_numero and tiene_caracter_especial
