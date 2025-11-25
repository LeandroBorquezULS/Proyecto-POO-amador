"""
main.py

Punto de entrada de la aplicación. Inicializa controlador y vista,
y fuerza la creación de contraseña admin la primera vez que se ejecuta.
"""

import tkinter as tk
from tkinter import simpledialog, messagebox
from controller import AppController
from view import InterfazAmador
import auth


def main():
    """Inicia la aplicación, solicita establecer contraseña si es la primera ejecución."""
    root = tk.Tk()
    controller = AppController()

    # Si no existe contraseña, pedir que el usuario cree una segura
    if not controller.existe_contrasena():
        messagebox.showinfo("Configuración inicial", "No se encontró contraseña de administrador. Debes crear una ahora.")
        while True:
            pwd = simpledialog.askstring("Crear contraseña", "Ingrese nueva contraseña (mínimo 6 caracteres):", show='*', parent=root)
            if pwd is None:
                messagebox.showerror("Imposible continuar", "La aplicación requiere una contraseña admin para operar. Cerrando.")
                root.destroy()
                return
            if len(pwd) < 6:
                messagebox.showwarning("Contraseña débil", "La contraseña debe tener al menos 6 caracteres.")
                continue
            pwd_confirm = simpledialog.askstring("Confirmar", "Confirma la contraseña:", show='*', parent=root)
            if pwd_confirm != pwd:
                messagebox.showwarning("No coinciden", "Las contraseñas no coinciden. Intenta de nuevo.")
                continue
            controller.establecer_contrasena(pwd)
            messagebox.showinfo("Listo", "Contraseña establecida correctamente.")
            break

    app = InterfazAmador(root, controller)
    app.pack(fill="both", expand=True)
    root.mainloop()


if __name__ == "__main__":
    main()
