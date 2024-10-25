# pedir al usuario que indrodusca el nombre
nombre = input("introduce tu nombre: ")
# comprobar si ese nombre es del administrador
administrador = "camilo"
# si es igual es bienvenida personalizada
if nombre.lower == administrador:
    print("bienvenido, ", nombre, " !")
# si no, bienvenida general
else:
    print("bienvenido invitado")
