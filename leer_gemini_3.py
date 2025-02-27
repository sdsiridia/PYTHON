'''Leer correos no leidos y sacar su asunto, origen y cuerpo'''
import imaplib
import email
import time
import getpass
import re  # Importar el módulo re para expresiones regulares
# import pyfiglet  # mover la importacion al principio
from rich.live import Live  # mover la importacion al principio
from rich.table import Table  # mover la importacion al principio
import pyfiglet

# Constantes para mejorar la legibilidad y mantenimiento
PALABRA_NUMERO_ERRORES = "Número de errores:"
PALABRA_ERRORES = "Errores:"
PALABRA_NUMERO_ERRORES_CERO = "Número de errores: 0"
PALABRA_ERRORES_CERO = "Errores: 0"
# diccionario para guardar asuntos y cantidad de errores
dic_errores = {}

# Conectar a la cuenta de Gmail
try:
    mail = imaplib.IMAP4_SSL('imap.gmail.com')
except imaplib.IMAP4.error as e:
    print(f"Error al conectar con Gmail: {e}")
    exit()

# Pedir el usuario y la contraseña
USERNAME = input("Correo: ")
PASSWORD = getpass.getpass("Contraseña: ")

try:
    mail.login(USERNAME, PASSWORD)
except imaplib.IMAP4.error as e:
    print(f"Error de autenticación: {e}")
    exit()

# Seleccionar la bandeja de entrada
try:
    mail.select('inbox')
except imaplib.IMAP4.error as e:
    print(f"Error al seleccionar la bandeja de entrada: {e}")
    exit()

# Buscar correos no leídos
status, messages = mail.search(None, 'UNSEEN')

# Obtener la lista de IDs de correos no leídos
mail_ids = messages[0].split()
# print(mail_ids)
for mail_index, mail_id in enumerate(mail_ids):
    try:
        status, msg_data = mail.fetch(mail_id, '(RFC822)')
        for response_part in msg_data:
            if isinstance(response_part, tuple):
                msg = email.message_from_bytes(response_part[1])
                subject = msg['subject']
                from_original = msg['from']  # Guardar el from_ original.

                # Obtener el cuerpo del mensaje
                body = ""  # Inicializar body para que no de error.
                if msg.is_multipart():
                    for part in msg.walk():
                        if part.get_content_type() == 'text/plain':
                            body = part.get_payload(
                                decode=True).decode('latin-1')
                            break  # Salir después de encontrar la primera parte de texto plano
                else:
                    body = msg.get_payload(decode=True).decode('latin-1')

                def tiene_errores(body: str, mail_id: str) -> bool:
                    """Funcion para saber si un correo tiene errores."""
                    if PALABRA_NUMERO_ERRORES in body:
                        indice = body.find(PALABRA_NUMERO_ERRORES)
                        sub_body = body[indice +
                                        len(PALABRA_NUMERO_ERRORES):indice + 50]
                        try:
                            errores = int(sub_body.split(".")[0])
                        except ValueError:
                            print(
                                f"No se pudo convertir a int: {sub_body} en el correo {mail_id}")
                            return False
                        indice_2 = from_original.find('<')
                        from_con_fecha = from_original[:indice_2] + msg['Date']
                        dic_errores[from_con_fecha] = errores
                        if PALABRA_NUMERO_ERRORES_CERO not in body:
                            mail.store(mail_id, '-FLAGS', 'Seen')
                        return True
                    elif PALABRA_ERRORES in body:
                        indice = body.find(PALABRA_ERRORES)
                        sub_body = body[indice +
                                        len(PALABRA_ERRORES):indice + 50]
                        try:
                            errores = int(sub_body.split(".")[0])
                        except ValueError:
                            print(
                                f"No se pudo convertir a int: {sub_body} en el correo {mail_id}")
                            return False
                        indice_2 = from_original.find('<')
                        from_con_fecha = from_original[:indice_2] + msg['Date']
                        dic_errores[from_con_fecha] = errores
                        if PALABRA_ERRORES_CERO not in body:
                            mail.store(mail_id, '-FLAGS', 'Seen')
                        return True
                    else:
                        mail.store(mail_id, '-FLAGS', 'Seen')
                        return False

                tiene_errores(body, mail_id)
    except Exception as e:
        print(f"Error al procesar el mensaje {mail_id}: {e}")


mail.close()
mail.logout()
# creacion del titulo
# TEXTO = pyfiglet.figlet_format("Errores")
# print(TEXTO)import pyfiglet


TEXTO = pyfiglet.figlet_format("Backup", font="slant")
print(TEXTO)

# armamos la tabla para presentar los datos
# print(dic_errores)
if len(dic_errores) > 0:
    table = Table()
    table.add_column("Origen", justify="center")
    table.add_column("ERRORES", justify="center")
    contador_tabla = 0
    with Live(table, refresh_per_second=4):
        for clave, valor in dic_errores.items():
            contador_tabla += 1
            time.sleep(0.4)
            if valor == 0:
                table.add_row(
                    f"[bold green]{contador_tabla}.- {clave}[/bold green]",
                    f"[bold green]{valor}[/bold green] :smiley:"
                )
            else:
                table.add_row(
                    f"[bold red]{contador_tabla}.- {clave}[/bold red]",
                    f"[bold red]{valor}[/bold red] :pile_of_poo:"
                )
else:
    table1 = Table()
    table1.add_column("[bold green]MENSAJES[/bold green]", justify="center")
    with Live(table1, refresh_per_second=4):
        table1.add_row("[bold green]No hay MENSAJES[/bold green]:smiley:")
