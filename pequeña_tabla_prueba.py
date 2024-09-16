''' Crear tabla para mostrar datos de forma mas polija'''
# import random
import time
from rich.live import Live
from rich.table import Table

table = Table()
table.add_column("Rod Id")
table.add_column("Descripcion")

with Live(table, refresh_per_second=4):
    for row in range(12):
        time.sleep(0.4)
        table.add_row(f"{row}", "[green] LISTO")
