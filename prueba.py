import tkinter as tk
from tkinter import messagebox


def guardar_datos():
    email = email_entry.get()
    password = password_entry.get()
    messagebox.showinfo("Datos Guardados",
                        f"Email: {email}\nContraseña: {password}")
    # Aquí puedes usar las variables email y password como necesites


def salir():
    root.quit()


def on_enter(event):
    root.focus_get().invoke()


# Crear ventana
root = tk.Tk()
root.title("Login")
root.geometry("300x200")

# Etiquetas y campos de entrada
tk.Label(root, text="Email:").pack(pady=5)
email_entry = tk.Entry(root)
email_entry.pack(pady=5)

tk.Label(root, text="Contraseña:").pack(pady=5)
password_entry = tk.Entry(root, show="*")  # Ocultar contraseña
password_entry.pack(pady=5)

# Asociar tecla Enter al botón activo
root.bind("<Return>", on_enter)

# Contenedor para los botones
button_frame = tk.Frame(root)
button_frame.pack(pady=10)

guardar_btn = tk.Button(button_frame, text="Guardar", command=guardar_datos)
guardar_btn.pack(side=tk.LEFT, padx=5)

salir_btn = tk.Button(button_frame, text="Salir", command=salir)
salir_btn.pack(side=tk.LEFT, padx=5)

# Hacer que el botón "Guardar" sea el predeterminado
guardar_btn.focus()

# Ejecutar la ventana
root.mainloop()
