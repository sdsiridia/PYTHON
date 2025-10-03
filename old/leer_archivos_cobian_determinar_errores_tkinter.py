'''Leer correos no leidos y sacar su asunto, origen y cuerpo'''
import os
import csv
import re
from email.header import decode_header
import ssl
import imaplib
import email
import time
import tkinter as tk
from tkinter import messagebox
# import getpass
# import pyfiglet
from rich.live import Live
from rich.table import Table
from colorama import Fore, Style, init, Back

from funciones import gradient_text
# diccionario para guardar asuntos y cantidad de errores
dic_errores = {}


def leer_archivos(usuario, password, cadena_busqueda, segunda_condicion, archivo_csv="resultados.csv"):
    resultados = []

    contexto_ssl = ssl.create_default_context()
    servidor = imaplib.IMAP4_SSL(
        "imap.gmail.com", 993, ssl_context=contexto_ssl)
    servidor.login(usuario, password)
    servidor.select("inbox")

    # Buscar solo emails no leídos
    estado, mensajes = servidor.search(None, 'UNSEEN')
    mensajes = mensajes[0].split()

    for num in mensajes[::-1]:
        estado, datos = servidor.fetch(num, "(RFC822)")
        if estado != "OK":
            continue

        mensaje = email.message_from_bytes(datos[0][1])

        fecha = mensaje["Date"]
        sujeto = mensaje["Subject"]
        if sujeto:
            sujeto, encoding = decode_header(sujeto)[0]
            if isinstance(sujeto, bytes):
                sujeto = sujeto.decode(encoding if encoding else "utf-8")
        else:
            sujeto = "(Sin asunto)"

        # Obtener el cuerpo del email
        cuerpo = ""
        if mensaje.is_multipart():
            for parte in mensaje.walk():
                if parte.get_content_type() == "text/plain" and not parte.get("Content-Disposition"):
                    charset = parte.get_content_charset() or "utf-8"
                    cuerpo = parte.get_payload(decode=True).decode(
                        charset, errors="replace")
                    break
        else:
            charset = mensaje.get_content_charset() or "utf-8"
            cuerpo = mensaje.get_payload(decode=True).decode(
                charset, errors="replace")

        # Buscar la cadena principal y extraer 5 caracteres después
        coincidencia = re.search(
            re.escape(cadena_busqueda) + r"(.{0,5})", cuerpo)

        if coincidencia:
            errores = coincidencia.group(1).strip()
            if segunda_condicion in cuerpo:
                # Coinciden ambas condiciones → marcar como leído y guardar
                resultados.append({
                    "fecha": fecha,
                    "sujeto": sujeto,
                    "errores": errores
                })
                servidor.store(num, '+FLAGS', '\\Seen')
            else:
                # No cumple segunda condición → mantener como no leído
                servidor.store(num, '-FLAGS', '\\Seen')
        else:
            # No se encuentra la primera cadena → mantener como no leído
            servidor.store(num, '-FLAGS', '\\Seen')

    servidor.logout()

    # Guardar resultados en CSV
    if resultados:
        existe = os.path.exists(archivo_csv)
        with open(archivo_csv, mode='a', newline='', encoding='utf-8') as archivo:
            campos = ["fecha", "sujeto", "errores"]
            escritor = csv.DictWriter(archivo, fieldnames=campos)
            if not existe:
                escritor.writeheader()
            escritor.writerows(resultados)

    return resultados


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
        leer_archivos(username, password, "Numero de errores:", "0")

    except Exception as e:
        messagebox.showerror("Error", str(e))
    # Aquí puedes usar las variables email y password como necesites

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
