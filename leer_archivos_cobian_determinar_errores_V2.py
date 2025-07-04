'''Leer correos no leidos y sacar su asunto, origen y cuerpo'''
import imaplib
import email
import time
import getpass
from tqdm import tqdm

from colorama import Fore, init  # , Style, Back
import pyfiglet
from rich.console import Console
from rich.live import Live
from rich.table import Table
from funciones import gradient_text, marcar_no_leido


# diccionario para guardar asuntos y cantidad de errores
dic_errores = {}

# Conectar a la cuenta de Gmail
mail = imaplib.IMAP4_SSL('imap.gmail.com')

# Pedir el usuario y la contraseña
USERNAME = input("Correo: ")
PASSWORD = getpass.getpass("Contraseña: ")
mail.login(USERNAME, PASSWORD)

# Seleccionar la bandeja de entrada
mail.select('inbox')

# Buscar correos no leídos
status, messages = mail.search(None, 'UNSEEN')

# Obtener la lista de IDs de correos no leídos
mail_ids = messages[0].split()
mail_num = len(mail_ids)
# print(f "Se encontraron {mail_num} correos no leídos")
# for i, mail_id in enumerate(mail_ids):
for i, mail_id in enumerate(tqdm(mail_ids, desc="Leyendo correos")):
    status, msg_data = mail.fetch(mail_id, '(RFC822)')
    for response_part in msg_data:
        if isinstance(response_part, tuple):
            msg = email.message_from_bytes(response_part[1])
            subject = msg['subject']
            from_ = msg['from']
            # print(msg['from'])
            # ============print de control============
            # print(f'From: {from_}\nSubject: {subject}\n')
            # Obtener el cuerpo del mensaje
            if msg.is_multipart():
                for part in msg.walk():
                    if part.get_content_type() == 'text/plain':
                        # he quitado el .decode()
                        body = part.get_payload(decode=True).decode('latin-1')
                        # ============print de control============
                        # print('\n=================\nMultipart\n=================\n')
                        # print(f'Body: {body}\n')
                        # print('\n=================\nMultipart\n=================\n')
                        # voy a intentar encontrar las palabras para podeer filtrar
                        if 'Número de errores:' in body:
                            indice = body.find("Número de errores:")
                            sub_body = body[indice+19:indice + 50]
                            errores = int(sub_body.split(".")[0])
                            # print(f"La cantidad de errores es: {errores}")
                            indice_2 = from_.find('<')
                            from_ = from_[:indice_2] + msg['Date']
                            dic_errores[from_] = errores
                            if 'Número de errores: 0' not in body:
                                marcar_no_leido(mail, mail_id)
                        elif 'Errores:' in body:
                            indice = body.find("Errores:")
                            sub_body = body[indice+9:indice + 50]
                            errores = int(sub_body.split(".")[0])
                            # print(f"La cantidad de errores es: {errores}")
                            # subject = subject[5:]
                            # dic_errores[subject] = errores
                            indice_2 = from_.find('<')
                            from_ = from_[:indice_2] + msg['Date']
                            dic_errores[from_] = errores
                            if 'Errores: 0' not in body:
                                marcar_no_leido(mail, mail_id)
                        else:
                            marcar_no_leido(mail, mail_id)
                            # mail.store(mail_id, '-FLAGS', '\\Seen')

            else:
                body = msg.get_payload(decode=True).decode()
                if 'Número de errores:' in body:
                    indice = body.find("Número de errores:")
                    sub_body = body[indice+19:indice + 50]
                    errores = int(sub_body.split(".")[0])
                    # print(f"La cantidad de errores es: {errores}")
                    # subject = subject[5:]
                    # dic_errores[subject] = errores
                    indice_2 = from_.find('<')
                    from_ = from_[:indice_2] + msg['Date']
                    dic_errores[from_] = errores
                    if 'Número de errores: 0' not in body:
                        marcar_no_leido(mail, mail_id)
                        # mail.store(mail_id, '-FLAGS', '\\SEEN')
                elif 'Errores:' in body:
                    indice = body.find("Errores:")
                    sub_body = body[indice+9:indice + 50]
                    errores = int(sub_body.split(".")[0])
                    # print(f"La cantidad de errores es: {errores}")
                    # subject = subject[5:]
                    # dic_errores[subject] = errores
                    indice_2 = from_.find('<')
                    from_ = from_[:indice_2] + msg['Date']
                    dic_errores[from_] = errores
                    if 'Errores: 0' not in body:
                        marcar_no_leido(mail, mail_id)
                        # mail.store(mail_id, '-FLAGS', '\\Seen')
                else:
                    marcar_no_leido(mail, mail_id)
                    # mail.store(mail_id, '-FLAGS', '\\Seen')
                # ============print de control============
                # print('\n=================\nnormal\n=================\n')
                # print(f'Body: {body}\n')
                # print('\n=================\nnormal\n=================\n')
# por si quiero parar en una cantidad de mensajes especifico
    # if i > 1:
    #     break
mail.close()
mail.logout()


# Definir colores ANSI para el degradado
gradient_colors = [
    Fore.RED, Fore.YELLOW, Fore.GREEN, Fore.CYAN, Fore.BLUE, Fore.MAGENTA
]

# Generar texto con pyfiglet
ascii_text = pyfiglet.figlet_format("Backup", font="slant")

TEXTO = gradient_text(ascii_text, gradient_colors)
# Aplicar el degradado


# print(TEXTO)
# armamos la tabla para presentar los datos
print(dic_errores)
if len(dic_errores) > 0:
    dic_errores_num = len(dic_errores)  # para contar la cantidad de errores
    init()
    print(TEXTO)
    table = Table()
    table.add_column("Origen", justify="center")
    table.add_column("ERRORES", justify="center")
    i = 0
    with Live(table, refresh_per_second=4):
        for clave, valor in dic_errores.items():

            i = i+1
            time.sleep(0.4)
            if valor == 0:
                table.add_row(f"[bold green]{i}.- {clave}[/bold green]", f"[bold green] {
                    valor}[/bold green] :smiley:")
            else:
                table.add_row(f"[bold red]{i}.- {clave}[/bold red]", f"[bold red] {
                    valor}[/bold red] :pile_of_poo:")
else:
    init()
    print(TEXTO)
    table1 = Table()
    table1.add_column("[bold green]MENSAJES[/bold green]", justify="center")
    with Live(table1, refresh_per_second=4):
        table1.add_row("[bold green]No hay MENSAJES[/bold green]:smiley:")
