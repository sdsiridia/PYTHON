import imaplib
import email
import getpass
from email.header import decode_header

# Configuración de la cuenta
# EMAIL = "tuemail@gmail.com"
# PASSWORD = "tupassword_o_contraseña_de_aplicación"
IMAP_SERVER = "imap.gmail.com"

# Pedir el usuario y la contraseña
EMAIL = input("Correo: ")
PASSWORD = getpass.getpass("Contraseña: ")

# Palabra clave que debe estar en el correo
PALABRA_CLAVE = "Número"


def conectar_imap():
    """Conectar a la cuenta de Gmail con IMAP."""
    mail = imaplib.IMAP4_SSL(IMAP_SERVER)
    mail.login(EMAIL, PASSWORD)
    return mail


def obtener_correos(mail):
    """Buscar correos no leídos en la bandeja de entrada."""
    mail.select("inbox")
    status, mensajes = mail.search(None, 'UNSEEN')  # Solo los no leídos
    return mensajes[0].split()  # Lista de IDs de correos


def leer_correo(mail, email_id):
    """Obtener el contenido del correo."""
    status, data = mail.fetch(email_id, "(RFC822)")
    for response_part in data:
        if isinstance(response_part, tuple):
            msg = email.message_from_bytes(response_part[1])
            subject, encoding = decode_header(msg["Subject"])[0]
            if isinstance(subject, bytes):
                subject = subject.decode(encoding or "utf-8")

            body = ""
            if msg.is_multipart():
                for part in msg.walk():
                    content_type = part.get_content_type()
                    content_disposition = str(part.get("Content-Disposition"))

                    if content_type == "text/plain" and "attachment" not in content_disposition:
                        body = part.get_payload(decode=True).decode()
                        break
            else:
                body = msg.get_payload(decode=True).decode()

            return subject, body
    return "", ""


def marcar_no_leido(mail, email_id):
    """Marcar un correo como no leído."""
    mail.store(email_id, "-FLAGS", "\\Seen")


def procesar_correos():
    """Leer correos y marcar como no leídos si no contienen la palabra clave."""
    mail = conectar_imap()
    correos = obtener_correos(mail)

    for email_id in correos:
        subject, body = leer_correo(mail, email_id)

        if PALABRA_CLAVE.lower() not in body.lower():
            marcar_no_leido(mail, email_id)
            print(f"Correo '{subject}' marcado como NO LEÍDO")

    mail.logout()


if __name__ == "__main__":
    procesar_correos()
