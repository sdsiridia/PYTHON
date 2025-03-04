'''Leer correos no leidos y sacar su asunto, origen y cuerpo'''
from colorama import Fore, Style, init, Back
import imaplib
import email
import time
import getpass
import pyfiglet
import tkinter as tk
from tkinter import messagebox
from rich.live import Live
from rich.table import Table
from funciones import gradient_text

# diccionario para guardar asuntos y cantidad de errores
dic_errores = {}


def salir():
    '''salir de la aplicacion'''
    root.quit()


def on_enter(event):
    '''guardar datos al presionar enter'''
    root.focus_get().invoke()


def guardar_datos():
    '''guardar datos en variables'''
    username = email_entry.get()
    password = password_entry.get()

    try:
        # Conectar a la cuenta de Gmail
        mail = imaplib.IMAP4_SSL('imap.gmail.com')

        mail.login(username, password)

        # Seleccionar la bandeja de entrada
        mail.select('inbox')

        # Buscar correos no leídos
        status, messages = mail.search(None, 'UNSEEN')
# # Conectar a la cuenta de Gmail
# mail = imaplib.IMAP4_SSL('imap.gmail.com')

# # Pedir el usuario y la contraseña
# USERNAME = input("Correo: ")
# PASSWORD = getpass.getpass("Contraseña: ")
# mail.login(USERNAME, PASSWORD)

# # Seleccionar la bandeja de entrada
# mail.select('inbox')

# # Buscar correos no leídos
# status, messages = mail.search(None, 'UNSEEN')

# # Obtener la lista de IDs de correos no leídos
# mail_ids = messages[0].split()
# # print(mail_ids)
# for i, mail_id in enumerate(mail_ids):
#     status, msg_data = mail.fetch(mail_id, '(RFC822)')
#     for response_part in msg_data:
#         if isinstance(response_part, tuple):
#             msg = email.message_from_bytes(response_part[1])
#             subject = msg['subject']
#             from_ = msg['from']
#             # print(msg['from'])
#             # ============print de control============
#             # print(f'From: {from_}\nSubject: {subject}\n')
#             # Obtener el cuerpo del mensaje
#             if msg.is_multipart():
#                 for part in msg.walk():
#                     if part.get_content_type() == 'text/plain':
#                         # he quitado el .decode()
#                         body = part.get_payload(decode=True).decode('latin-1')
#                         # ============print de control============
#                         # print('\n=================\nMultipart\n=================\n')
#                         # print(f'Body: {body}\n')
#                         # print('\n=================\nMultipart\n=================\n')
#                         # voy a intentar encontrar las palabras para podeer filtrar
#                         if 'Número de errores:' in body:
#                             indice = body.find("Número de errores:")
#                             sub_body = body[indice+19:indice + 50]
#                             errores = int(sub_body.split(".")[0])
#                             # print(f"La cantidad de errores es: {errores}")
#                             indice_2 = from_.find('<')
#                             from_ = from_[:indice_2] + msg['Date']
#                             dic_errores[from_] = errores
#                         else:
#                             mail.store(mail_id, '-FLAGS', '\\Seen')


#             else:
#                 body = msg.get_payload(decode=True).decode()
#                 if 'Número de errores:' in body:
#                     indice = body.find("Número de errores:")
#                     sub_body = body[indice+19:indice + 50]
#                     errores = int(sub_body.split(".")[0])
#                     # print(f"La cantidad de errores es: {errores}")
#                     # subject = subject[5:]
#                     # dic_errores[subject] = errores
#                     indice_2 = from_.find('<')
#                     from_ = from_[:indice_2] + msg['Date']
#                     dic_errores[from_] = errores
#                     if 'Número de errores: 0' not in body:
#                         mail.store(mail_id, '-FLAGS', '\\Seen')
#                 elif 'Errores:' in body:
#                     indice = body.find("Errores:")
#                     sub_body = body[indice+9:indice + 50]
#                     errores = int(sub_body.split(".")[0])
#                     # print(f"La cantidad de errores es: {errores}")
#                     # subject = subject[5:]
#                     # dic_errores[subject] = errores
#                     indice_2 = from_.find('<')
#                     from_ = from_[:indice_2] + msg['Date']
#                     dic_errores[from_] = errores
#                     if 'Errores: 0' not in body:
#                         mail.store(mail_id, '-FLAGS', '\\Seen')
#                 else:
#                     mail.store(mail_id, '-FLAGS', '\\Seen')
#                 # ============print de control============
#                 # print('\n=================\nnormal\n=================\n')
#                 # print(f'Body: {body}\n')
#                 # print('\n=================\nnormal\n=================\n')

    except Exception as e:
        messagebox.showerror("Error", str(e))
    # Aquí puedes usar las variables email y password como necesites

    mail.close()
    mail.logout()
    # hasta aca ---------------
    print(dic_errores)


# Crear ventana
root = tk.Tk()
root.title("Login")
root.geometry("300x200")

# Etiquetas y campos de entrada
tk.Label(root, text="Email:").pack(pady=5)
email_entry = tk.Entry(root)
email_entry.pack(pady=5)

tk.Label(root, text="Contraseña:").pack(pady=5)
password_entry = tk.Entry(root, show="*")  # Ocultar contraseña
password_entry.pack(pady=5)

# Asociar tecla Enter al botón activo
root.bind("<Return>", on_enter)

# Contenedor para los botones
button_frame = tk.Frame(root)
button_frame.pack(pady=10)

guardar_btn = tk.Button(button_frame, text="Guardar", command=guardar_datos)
guardar_btn.pack(side=tk.LEFT, padx=5)

salir_btn = tk.Button(button_frame, text="Salir", command=salir)
salir_btn.pack(side=tk.LEFT, padx=5)

# Hacer que el botón "Guardar" sea el predeterminado
# guardar_btn.focus()

# hacer que el primer boton sea el predeterminado
email_entry.focus()

# Ejecutar la ventana
root.mainloop()


# armamos la tabla para presentar los datos
# print(dic_errores)
if len(dic_errores) > 0:
    init()

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
    table1 = Table()
    table1.add_column("[bold green]MENSAJES[/bold green]", justify="center")
    with Live(table1, refresh_per_second=4):
        table1.add_row("[bold green]No hay MENSAJES[/bold green]:smiley:")
