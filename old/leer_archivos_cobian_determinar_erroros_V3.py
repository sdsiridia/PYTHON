'''leer_correos_no_leidos_y_sacar_su_origen_y_cuerpo'''
import imaplib
import email
# import time
import getpass
from colorama import Fore, init
import pyfiglet
from rich.console import Console
from rich.table import Table
from rich.progress import (
    Progress, SpinnerColumn, BarColumn, TextColumn, TimeRemainingColumn
)
from funciones import gradient_text, marcar_no_leido

# ========== CONFIG ==========
console = Console()
dic_errores = {}  # diccionario para guardar asuntos y cantidad de errores

# ========== CONEXIÓN ==========
mail = imaplib.IMAP4_SSL('imap.gmail.com')
USERNAME = input("Correo: ")
PASSWORD = getpass.getpass("Contraseña: ")
mail.login(USERNAME, PASSWORD)
mail.select('inbox')
status, messages = mail.search(None, 'UNSEEN')
mail_ids = []
if messages and len(messages) > 0:
    mail_ids = messages[0].split()
mail_num = len(mail_ids)

# ========== PROCESAR CORREOS CON BARRA DE PROGRESO ==========
with Progress(
    SpinnerColumn(),
    TextColumn("[bold blue]{task.description}"),
    BarColumn(),
    "[progress.percentage]{task.percentage:>3.1f}%",
    TimeRemainingColumn(),
    transient=True
) as progress:
    task = progress.add_task("Leyendo correos...", total=len(mail_ids))

    for mail_id in mail_ids:
        status, msg_data = mail.fetch(mail_id, '(RFC822)')
        for response_part in msg_data:
            if isinstance(response_part, tuple) and len(response_part) > 1:
                msg = email.message_from_bytes(response_part[1])
                subject = msg['subject']
                from_ = msg['from']

                # Obtener el cuerpo del mensaje
                if msg.is_multipart():
                    for part in msg.walk():
                        if part.get_content_type() == 'text/plain':
                            body = part.get_payload(
                                decode=True).decode('latin-1')
                            if 'Número de errores:' in body:
                                indice = body.find("Número de errores:")
                                sub_body = body[indice+19:indice + 50]
                                errores = int(sub_body.split(".")[0])
                                indice_2 = from_.find('<')
                                from_ = from_[:indice_2] + msg['Date']
                                dic_errores[from_] = errores
                                if errores != 0:
                                    marcar_no_leido(mail, mail_id)
                            elif 'Errores:' in body:
                                indice = body.find("Errores:")
                                sub_body = body[indice+9:indice + 50]
                                errores = int(sub_body.split(".")[0])
                                indice_2 = from_.find('<')
                                from_ = from_[:indice_2] + msg['Date']
                                dic_errores[from_] = errores
                                if errores != 0:
                                    marcar_no_leido(mail, mail_id)
                            else:
                                marcar_no_leido(mail, mail_id)
                else:
                    body = msg.get_payload(decode=True).decode()
                    if 'Número de errores:' in body:
                        indice = body.find("Número de errores:")
                        sub_body = body[indice+19:indice + 50]
                        errores = int(sub_body.split(".")[0])
                        indice_2 = from_.find('<')
                        from_ = from_[:indice_2] + msg['Date']
                        dic_errores[from_] = errores
                        if errores != 0:
                            marcar_no_leido(mail, mail_id)
                    elif 'Errores:' in body:
                        indice = body.find("Errores:")
                        sub_body = body[indice+9:indice + 50]
                        errores = int(sub_body.split(".")[0])
                        indice_2 = from_.find('<')
                        from_ = from_[:indice_2] + msg['Date']
                        dic_errores[from_] = errores
                        if errores != 0:
                            marcar_no_leido(mail, mail_id)
                    else:
                        marcar_no_leido(mail, mail_id)

        progress.update(task, advance=1)

mail.close()
mail.logout()

# ========== TÍTULO ESTILO FIGLET ==========
gradient_colors = [Fore.RED, Fore.YELLOW,
                   Fore.GREEN, Fore.CYAN, Fore.BLUE, Fore.MAGENTA]
ascii_text = pyfiglet.figlet_format("Backup", font="slant")
TEXTO = gradient_text(ascii_text, gradient_colors)


# ========== MOSTRAR TABLA FINAL CON CONTADOR Y DETALLES ==========
init()
print(TEXTO)

if dic_errores:
    total_errores = sum(dic_errores.values())

    table = Table(title="[bold]Errores detectados[/bold]")
    table.add_column("Origen", justify="left", style="cyan")
    table.add_column("ERRORES", justify="center", style="bold")

    with Progress(
        SpinnerColumn(),
        TextColumn("[bold green]{task.description}"),
        BarColumn(),
        "[progress.percentage]{task.percentage:>3.1f}%",
        TimeRemainingColumn(),
        transient=True
    ) as progress:
        task = progress.add_task("Generando tabla...", total=len(dic_errores))

        for i, (clave, valor) in enumerate(dic_errores.items(), start=1):
            # time.sleep(1)  # <-- Delay aquí
            if valor == 0:
                ICONO = ":white_check_mark:"
                table.add_row(
                    f"[bold green]{i}.- {clave}[/bold green]",
                    f"[bold green]{valor}[/bold green] {ICONO}"
                )
            elif valor <= 3:
                ICONO = ":pile_of_poo:"
                table.add_row(
                    f"[bold yellow]{i}.- {clave}[/bold yellow]",
                    f"[bold yellow]{valor}[/bold yellow] {ICONO}"
                )
            else:
                ICONO = ":x:"
                table.add_row(
                    f"[bold red]{i}.- {clave}[/bold red]",
                    f"[bold red]{valor}[/bold red] {ICONO}"
                )
            progress.update(task, advance=1)

    console.print(table)

    # Mostrar resumen final de errores
    if total_errores > 0:
        console.print(
            f"\n[bold red]🔴 Se detectaron un total de {total_errores} errores 🛠️[/bold red]")
    else:
        console.print(
            "\n[bold green]🟢 ¡Todo está bien! No se detectaron errores 😄[/bold green]")

else:
    table = Table()
    table.add_column("[bold green]MENSAJES[/bold green]", justify="center")
    table.add_row("[bold green]No hay MENSAJES[/bold green] :smiley:")
    console.print(table)


# Contamos para gráfico #
if dic_errores:
    bien = sum(1 for v in dic_errores.values() if v == 0)
    mal = sum(1 for v in dic_errores.values() if v != 0)
    total = bien + mal
    porc_bien = round((bien / total) * 100, 1)
    porc_mal = round((mal / total) * 100, 1)

    # Creamos consola
    console = Console()

    # Simulación de torta con barra coloreada
    console.print("\n[bold]Grafico de errores:[/bold]")
    console.print(
        f"[green] {'█' * int(porc_bien // 2)}[/green][red]{'█' * int(porc_mal // 2)}[/red]")

    # Texto extra
    console.print(
        f"[green]Bien: {porc_bien}%[/green]  [red]Mal: {porc_mal}%[/red]")


# # ========== MOSTRAR TABLA FINAL otro metodo==========
# init()
# print(TEXTO)

# if dic_errores:
#     table = Table(title="[bold]Errores detectados[/bold]")
#     table.add_column("Origen", justify="center")
#     table.add_column("ERRORES", justify="center")

#     with Progress(
#         SpinnerColumn(),
#         TextColumn("[bold green]{task.description}"),
#         BarColumn(),
#         "[progress.percentage]{task.percentage:>3.1f}%",
#         TimeRemainingColumn(),
#         transient=True
#     ) as progress:
#         task = progress.add_task("Generando tabla...", total=len(dic_errores))

#         for i, (clave, valor) in enumerate(dic_errores.items(), start=1):
#             if valor == 0:
#                 table.add_row(f"[bold green]{i}.- {clave}[/bold green]",
#                               f"[bold green]{valor}[/bold green] :smiley:")
#             else:
#                 table.add_row(f"[bold red]{i}.- {clave}[/bold red]",
#                               f"[bold red]{valor}[/bold red] :pile_of_poo:")
#             progress.update(task, advance=1)

#     console.print(table)

# else:
#     table = Table()
#     table.add_column("[bold green]MENSAJES[/bold green]", justify="center")
#     table.add_row("[bold green]No hay MENSAJES[/bold green] :smiley:")
#     console.print(table)
