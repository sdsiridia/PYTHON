'''Leer correos no leidos y sacar su asunto, orign y cuerpo'''
import imaplib
import email
import time
import getpass
from rich.live import Live
from rich.table import Table
from rich import print

# diccionario para guardar asuntos y cantidad de errores
dic_errores = {}

# Conectar a la cuenta de Gmail
mail = imaplib.IMAP4_SSL('imap.gmail.com')
USERNAME = input("Correo: ")
PASSWORD = getpass.getpass("Contraseña: ")
mail.login(USERNAME, PASSWORD)

# Seleccionar la bandeja de entrada
mail.select('inbox')

# Buscar correos no leídos
status, messages = mail.search(None, 'UNSEEN')

# Obtener la lista de IDs de correos no leídos
mail_ids = messages[0].split()
# print(mail_ids)
for i, mail_id in enumerate(mail_ids):
    status, msg_data = mail.fetch(mail_id, '(RFC822)')
    for response_part in msg_data:
        if isinstance(response_part, tuple):
            msg = email.message_from_bytes(response_part[1])
            subject = msg['subject']
            from_ = msg['from']
            # print de control
            # print(f'From: {from_}\nSubject: {subject}\n')

            # Obtener el cuerpo del mensaje
            if msg.is_multipart():
                for part in msg.walk():
                    if part.get_content_type() == 'text/plain':
                        # he quitado el .decode()
                        body = part.get_payload(decode=True).decode('latin-1')
                        # print de control
                        # print('\n=================\nMultipart\n=================\n')
                        # print(f'Body: {body}\n')
                        # print('\n=================\nMultipart\n=================\n')
                        # voy a intentar encontrar las palabras para podeer filtrar
                        if 'Número de errores:' in body:
                            indice = body.find("Número de errores:")
                            sub_body = body[indice+19:indice + 50]
                            errores = int(sub_body.split(".")[0])
                            # print(f"La cantidad de errores es: {errores}")

                            # subject = subject[5:]
                            # dic_errores[subject] = errores
                            dic_errores[from_] = errores
                        else:
                            mail.store(mail_id, '-FLAGS', '\\Seen')

            else:
                body = msg.get_payload(decode=True).decode()
                if 'Número de errores:' in body:
                    indice = body.find("Número de errores:")
                    sub_body = body[indice+19:indice + 50]
                    errores = int(sub_body.split(".")[0])
                    # print(f"La cantidad de errores es: {errores}")
                    # subject = subject[5:]
                    # dic_errores[subject] = errores
                    dic_errores[from_] = errores
                else:
                    mail.store(mail_id, '-FLAGS', '\\Seen')
                # print de control
                # print('\n=================\nnormal\n=================\n')
                # print(f'Body: {body}\n')
                # print('\n=================\nnormal\n=================\n')
# porsi quiero parar en una cantidad de mensajes especifico
# if i > 1:
#     break
mail.close()
mail.logout()
# armamos la tabla para presentar los datos
# print(dic_errores)
table = Table()
table.add_column("Origen")
table.add_column("ERRORES")

with Live(table, refresh_per_second=4):
    for clave, valor in dic_errores.items():
        time.sleep(0.4)
        if valor == 0:
            table.add_row(f"[bold green]{clave}[/bold green]", f"[bold green] {
                          valor}[bold green] :smiley:")
        else:
            table.add_row(f"[bold red]{clave}[/bold red]", f"[bold red] {
                          valor}[/bold red] :pile_of_poo:")

'''
Imprime por consola una tabla
from rich.console import Console
from rich.table import Table

table = Table(title="Star Wars Movies")
table.add_column("Released", justify="right", style="cyan", no_wrap=True)
table.add_column("Title", style="magenta")
table.add_column("Box Office", justify="right", style="green")
table.add_row("Dec 20, 2019",
              "Star Wars: The Rise of Skywalker", "$952,110,690")
table.add_row("May 25, 2018", "Solo: A Star Wars Story", "$393,151,347")
table.add_row("Dec 15, 2017",
              "Star Wars Ep. V111: The Last Jedi", "$1,332,539,889")
table.add_row("Dec 16, 2016", "Rogue One: A Star Wars Story", "$1,332,439,889")
console = Console()
console.print(table)
'''