'''Leer correos no leidos y sacar su asunto, orign y cuerpo'''
import imaplib
import email

# Conectar a la cuenta de Gmail
mail = imaplib.IMAP4_SSL('imap.gmail.com')
mail.login('sdsiridia@gmail.com', 'ljtckojprksyeiyz')

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
            print(f'From: {from_}\nSubject: {subject}\n')

            # Obtener el cuerpo del mensaje
            if msg.is_multipart():
                for part in msg.walk():
                    if part.get_content_type() == 'text/plain':
                        body = part.get_payload(decode=True).decode()
                        print('\n=================\nMultipart\n=================\n')
                        print(f'Body: {body}\n')
                        print('\n=================\nMultipart\n=================\n')
                        if 'personas' in body:
                            print(' palabra encontrada')
            else:
                body = msg.get_payload(decode=True).decode()
                print('\n=================\nnormal\n=================\n')
                print(f'Body: {body}\n')
                print('\n=================\nnormal\n=================\n')
    if i > 3:
        break
