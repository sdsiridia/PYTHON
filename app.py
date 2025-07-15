from flask import Flask, render_template, request, redirect, url_for
import imaplib
import email
from funciones import marcar_no_leido  # Usa tu archivo original
from datetime import datetime

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        correo = request.form["correo"]
        contrasena = request.form["contrasena"]

        errores_dict = {}
        try:
            mail = imaplib.IMAP4_SSL('imap.gmail.com')
            mail.login(correo, contrasena)
            mail.select("inbox")
            status, messages = mail.search(None, "UNSEEN")
            mail_ids = messages[0].split()

            for mail_id in mail_ids:
                status, msg_data = mail.fetch(mail_id, "(RFC822)")
                for response_part in msg_data:
                    if isinstance(response_part, tuple):
                        msg = email.message_from_bytes(response_part[1])
                        subject = msg["subject"]
                        from_ = msg["from"]
                        date_ = msg["Date"]

                        # Obtener cuerpo
                        if msg.is_multipart():
                            for part in msg.walk():
                                if part.get_content_type() == "text/plain":
                                    body = part.get_payload(
                                        decode=True).decode("latin-1")
                                    errores = extraer_errores(body)
                                    if errores is not None:
                                        errores_dict[f"{from_} ({date_})"] = errores
                                        if errores != 0:
                                            marcar_no_leido(mail, mail_id)
                        else:
                            body = msg.get_payload(
                                decode=True).decode("latin-1")
                            errores = extraer_errores(body)
                            if errores is not None:
                                errores_dict[f"{from_} ({date_})"] = errores
                                if errores != 0:
                                    marcar_no_leido(mail, mail_id)

            mail.logout()

        except Exception as e:
            return render_template("index.html", error=str(e))

        return render_template("resultados.html", errores=errores_dict)

    return render_template("index.html")


def extraer_errores(body):
    if "Número de errores:" in body:
        try:
            idx = body.find("Número de errores:") + 19
            sub = body[idx:idx+30].split(".")[0]
            return int(sub.strip())
        except:
            return None
    elif "Errores:" in body:
        try:
            idx = body.find("Errores:") + 9
            sub = body[idx:idx+30].split(".")[0]
            return int(sub.strip())
        except:
            return None
    return None


if __name__ == "__main__":
    app.run(debug=True)
