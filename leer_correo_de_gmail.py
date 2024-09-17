'''Leer correo de Gmail'''

import imaplib
import email
from email.header import decode_header  # metodo para leer el encabezado
import webbrowser
import os
import getpass
# import getpass -> PARA USAR CUANDO QUEREMOS ESCRIBIR LA CONTRASEÑA
# Y NO PASARLA COMO PARAMETRO Y QUE SE ESCONDA LINEA 13

# Datos del usuario PODEMOS PEDIRLOS COMO MUESTRA
USERNAME = input("Correo: ")
PASSWORD = getpass.getpass("Contraseña: ")

# Crear conexión
imap = imaplib.IMAP4_SSL("imap.gmail.com")
# iniciar sesión
imap.login(USERNAME, PASSWORD)
#  lee siempre los email por fecha con la opcion
# ("INBOX",readonly=False) deberia saltearlos pero no lo hace
status, mensajes = imap.select("INBOX")
print(mensajes)  # -> podemos saber cuantos correos tenemmos
print('\n=============\n')
# mensajes a recibir
N = 3
# cantidad total de correos
can_mensajes = int(mensajes[0])

for i in range(can_mensajes, can_mensajes - N, -1):
    #    print(f"vamos por el mensaje: {i}")
    #     # Obtener el mensaje
    try:  # -> por si la cantidad de mensajes que quiero leer es superior a la que existen
        # fetch -> obtener el mensaje i RFC822 -> es un standar dice que voy as pedir todas las partes del mensaje
        # las variables res y mensaje es por que 'imap.fetch(str(i), "(RFC822)")'
        # nos devuelve la respuesta de la solicitud y el mensaje
        # srt(i) -> i es el numero de mensaje | metodo fetch pide un string
        res, mensaje = imap.fetch(str(i), "(RFC822)")
        # print(mensaje) -> para mostrar por consola los mensajes
        # está de una manera poco lejible
    # cuando nos referimos a un error especifco colocamos ImportError
    except ImportError:
        break
    for respuesta in mensaje:  # mensaje es una lista de todas las partes del correo
        # esto es una validación, para saber si respuesta es una tupla
        if isinstance(respuesta, tuple):
            # Obtener el contenido
            # parte del contenido son tuplas por ejemplo: subject : para maría
            # tupla ->(subject:'para maria')
            mensaje = email.message_from_bytes(respuesta[1])
            # decodificar el contenido | [0][0] -> para leer solo lo priemro
            subject = decode_header(mensaje["Subject"])[0][0]
            if isinstance(subject, bytes):
                # convertir a string usa la misma variable pero no es necesario
                subject = subject.decode()
            # de donde viene el correo
            from_ = mensaje.get("From")
            print("Asunto:", subject)
            print("From:", from_)
            print("******Mensaje obtenido con exito******")
            print("\n\n=====================\n\n")
#             # si el correo es html
# ------------------------------------------------------------------------
            if mensaje.is_multipart():
                # Recorrer las partes del correo
                for part in mensaje.walk():  # walk sirve para leer cada parte del mensaje
                    # Extraer el contenido
                    content_type = part.get_content_type()
                    CONTENT_DISPOSITION = str(part.get("Content-Disposition"))
                    try:
                        # el cuerpo del correo -> get_paylaod >---< quite .decode porque daba error
                        # igual mas abajo lo decodifico con el mismo metodo pero sobre
                        # la variable body revisar si es asi
                        #  lo he quitado por que da error
                        # .decode('utf-8') lo he colocado en la linea 82
                        body = part.get_payload(
                            decode=True)

                    except ImportError:
                        pass
                    if content_type == "text/plain" and "attachment" not in CONTENT_DISPOSITION:
                        body = body.decode('utf-8')
                        print(body)
#                         # Mostrar el cuerpo del correo
                        nombre_archivo = part.get_filename()
                        if nombre_archivo:
                            if not os.path.isdir(subject):
                                # crear una carpeta para el mensaje
                                os.mkdir(subject)
                            ruta_archivo = os.path.join(
                                subject, nombre_archivo)

#                         print(str(body))
# leo el adjunto y lo guardo en una carpeta
                    elif "attachment" in CONTENT_DISPOSITION:
                        # download attachment y obtenemos el nombre
                        nombre_archivo = part.get_filename()
                        if nombre_archivo:
                            # corroboramos si existe la carpeta
                            if not os.path.isdir(subject):
                                # crear una carpeta para el mensaje
                                # con el nombre del asunto
                                os.mkdir(subject)
                                # la ruta del archivo que voy a crear
                                # lo hacemos asi para que sea compatible con multiples sistemas
                                # ya se linux windows etc
                                # os.path.join -> identifica el sistema operativo
                            ruta_archivo = os.path.join(
                                subject, nombre_archivo)
                            # descargamos el adjunto y lo guardamos
                            # se hace con 'wb' -> para que python lo escriba como bytes
                            with open(ruta_archivo, "wb") as file:
                                file.write(part.get_payload(decode=True))
# # ---------------------------------------------------------------------------
# # ahora agregamos una parte para reconocer el contenido html del mensaje como es debido
# # y no que lo pase como texto plano en la consola
# # si no tiene adjunto
            else:
                # contenido del mensaje
                content_type = mensaje.get_content_type()
                # cuerpo del mensaje decode=True decodifica el contenido
                body = mensaje.get_payload(decode=True).decode()
                if content_type == "text/plain":
                    # intento que guarde el cuerpo en un archivo
                    try:
                        with open(ruta_archivo, 'w', encoding='utf-8') as file:
                            file.write(body)
                    except ImportError:
                        pass
#                     # mostrar solo el texto
                    print(body)
            if content_type == "text/html":
                #                 # Abrir el html en el navegador
                if not os.path.isdir(subject):
                    os.mkdir(subject)
                    nombre_archivo = f"{subject}.html"
                    ruta_archivo = os.path.join(subject, nombre_archivo)
                with open(ruta_archivo, "w", encoding='utf-8') as file:
                    # decoded_string = body.decode('utf-8')
                    # por algun motivi da un error aunque funciona con la codificación
                    # 'utf-8' puedo cambiar la por 'latin-1' pero pierdo todo
                    # lo que embellece html y se queda como texto plano con caracteres extraños
                    decoded_string = body.decode('utf-8')
                    # decoded_string = str(body,'latin-1')
                    file.write(decoded_string)
#                 # abrir el navegador para mostrar el archivo
                webbrowser.open(ruta_archivo)
            print("********************************")
imap.close()
imap.logout()
