'''saber la hora de recepcion de un email'''
import imaplib
import email
from email.header import decode_header
import datetime
import getpass

# Configuración de la cuenta
USERNAME = input("Correo: ")
PASSWORD = getpass.getpass("Contraseña: ")

# Conectar a la cuenta de Gmail
mail = imaplib.IMAP4_SSL("imap.gmail.com")
mail.login(USERNAME, PASSWORD)
mail.select("inbox")

# Buscar correos electrónicos en la bandeja de entrada
status, messages = mail.search(None, "ALL")
email_ids = messages[0].split()

# Procesar los correos electrónicos
for email_id in email_ids:
    status, msg_data = mail.fetch(email_id, "(RFC822)")
    for response_part in msg_data:
        if isinstance(response_part, tuple):
            msg = email.message_from_bytes(response_part[1])
            date_tuple = email.utils.parsedate_tz(msg["Date"])
            if date_tuple:
                local_date = datetime.datetime.fromtimestamp(
                    email.utils.mktime_tz(date_tuple))
                print(f"Fecha de recepción: {
                      local_date.strftime('%Y-%m-%d %H:%M:%S')}")

# Cerrar la conexión
mail.close()
mail.logout()
