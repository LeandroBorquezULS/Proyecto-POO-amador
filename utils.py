"""
utils.py

Funciones auxiliares de la aplicación (envío de alerta WhatsApp).
La automatización con pyautogui es opcional: si no está instalada, se informa y
el envío no se realiza automáticamente.
"""

import time
import webbrowser
import threading
from tkinter import messagebox

# Intento aislado de dependencia pesada para no romper ejecución si falta
try:
    import pyautogui
except ImportError:
    pyautogui = None


def ejecutar_envio_whatsapp(numero_contacto: str, mensaje: str) -> None:
    """
    Abre WhatsApp Web para enviar un mensaje. Si pyautogui está disponible,
    intenta presionar 'enter' automáticamente después de abrir la url.

    Args:
        numero_contacto (str): Número en formato internacional sin '+' (ej: '56912345678').
        mensaje (str): Texto del mensaje.
    """
    # Construir URL segura (espacios y caracteres especiales codificados)
    import urllib.parse
    texto = urllib.parse.quote(mensaje)
    url = f"https://wa.me/{numero_contacto}?text={texto}"
    webbrowser.open(url)

    # Si no tenemos pyautogui, informamos al usuario y terminamos.
    if pyautogui is None:
        # Dejar que la UI maneje los mensajes (aquí solo mostramos mensaje simple)
        messagebox.showinfo("Acción iniciada", "Se abrió WhatsApp Web. Complete el envío manualmente.\n(Instale pyautogui para automatizar: pip install pyautogui)")
        return

    # Ejecutar secuencia en hilo aparte (no bloquear UI)
    def tarea():
        time.sleep(8)  # esperar a que cargue
        try:
            pyautogui.press('enter')
            time.sleep(1)
            pyautogui.press('enter')
        except Exception:
            # En caso de error con pyautogui, informar al usuario
            messagebox.showwarning("Automatización fallida", "No se pudo automatizar el envío con pyautogui. Envíe el mensaje manualmente.")

    threading.Thread(target=tarea, daemon=True).start()
