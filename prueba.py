import pyfiglet
from colorama import Fore, Style

# Función para generar un degradado de colores en ANSI


def gradient_text(text, colors):
    '''pintar de un color cada parte del texto'''
    colored_text = ""
    for i, char in enumerate(text):
        # Repetir colores en caso de que el texto sea más largo
        color = colors[i % len(colors)]
        colored_text += color + char
    return colored_text + Style.RESET_ALL


# Definir colores ANSI para el degradado
gradient_colors = [
    Fore.RED, Fore.YELLOW, Fore.GREEN, Fore.CYAN, Fore.BLUE, Fore.MAGENTA
]

# Generar texto con pyfiglet
ascii_text = pyfiglet.figlet_format("backup")

# Aplicar el degradado
colored_ascii = gradient_text(ascii_text, gradient_colors)

# Imprimir resultado
print(colored_ascii)
