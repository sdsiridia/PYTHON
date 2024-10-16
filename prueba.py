from rich.live import Live
from rich.table import Table
table1 = Table()
table1.add_column("Origen")
with Live(table1, refresh_per_second=4):
    table1.add_row("[bold green]No hay MENSAJES[/bold green]:smiley:")
