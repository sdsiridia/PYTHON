'''main'''
import validador
# import generador


def solicitar_contrasena_segura():
    '''pedido de ingreso de'''
    contrasena = input("Ingrese una contraseña: ")
    valida = validador.validar_contrasena(contrasena)

    if valida:
        print("Contraseña segura")

    else:
        print("La contraseña no es segura. Se sugiere una nueva contraseña")
        print("Sugerencia de contraseña: ")

# Ejemplo de uso


solicitar_contrasena_segura()
