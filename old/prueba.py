from rich.console import Console
from rich.progress import Progress, BarColumn, TextColumn
from rich.table import Table

# Datos de entrada
mi_diccionario = {
    'item1': 0,
    'item2': 3,
    'item3': 0,
    'item4': 2,
    'item5': 0,
    'item6': 5,
}

# Contamos
bien = sum(1 for v in mi_diccionario.values() if v == 0)
mal = sum(1 for v in mi_diccionario.values() if v != 0)
total = bien + mal
porc_bien = round((bien / total) * 100, 1)
porc_mal = round((mal / total) * 100, 1)

# Creamos consola
console = Console()

# Tabla resumen
table = Table(title="Resumen de Datos")
table.add_column("Estado", style="bold")
table.add_column("Cantidad", justify="right")
table.add_column("Porcentaje", justify="right")
table.add_row("✅ Bien (0)", str(bien), f"{porc_bien}%")
table.add_row("❌ Mal (!=0)", str(mal), f"{porc_mal}%")
console.print(table)

# Simulación de torta con barra coloreada
console.print("\n[bold]Simulación de Torta (de forma lineal):[/bold]")
console.print(
    f"[green] {'█' * int(porc_bien // 2)}[/green][red]{'█' * int(porc_mal // 2)}[/red]")

# Texto extra
console.print(
    f"[green]Bien: {porc_bien}%[/green]  [red]Mal: {porc_mal}%[/red]")
