''' Listado de funciones'''
import imaplib
# import email
from colorama import Style  # Fore, init, Back
# import time
# import getpass


def gradient_text(text, colors):
    '''pintar de un color cada parte del texto'''
    colored_text = ""
    for i, char in enumerate(text):
        # Repetir colores en caso de que el texto sea más largo
        color = colors[i % len(colors)]
        colored_text += color + char
    return colored_text + Style.RESET_ALL


def conectar_correo(username, password):
    '''conectar al correo'''
    mail = imaplib.IMAP4_SSL('imap.gmail.com')
    mail.login(username, password)
    return mail


def seleccionar_bandeja(mail):
    '''seleccionar la bandeja'''
    mail.select('inbox')
    return mail


def marcar_no_leido(mail, email_id):
    """Marcar un correo como no leído."""
    mail.store(email_id, "-FLAGS", "\\Seen")
