''' Listado de funciones'''
from colorama import Fore, Style, init, Back


def gradient_text(text, colors):
    '''pintar de un color cada parte del texto'''
    colored_text = ""
    for i, char in enumerate(text):
        # Repetir colores en caso de que el texto sea más largo
        color = colors[i % len(colors)]
        colored_text += color + char
    return colored_text + Style.RESET_ALL
