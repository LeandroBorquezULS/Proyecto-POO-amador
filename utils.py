"""
utils.py
"""
import time
import webbrowser
import urllib.parse

try:
    import pyautogui
except ImportError:
    pyautogui = None

import winsound

import sys
import os

def resource_path(relative_path):
    """ Obtiene la ruta absoluta al recurso, funciona para dev y PyInstaller """
    try:
        # PyInstaller crea una carpeta temporal en _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def reproducir_sonido_exito():
    """Reproduce el archivo de sonido checklist_ok.wav."""
    try:
        # Resolver ruta correcta (ya sea script o exe)
        archivo = resource_path("checklist_ok.wav")
        # Reproducir archivo WAV de forma asíncrona
        winsound.PlaySound(archivo, winsound.SND_FILENAME | winsound.SND_ASYNC)
    except Exception as e:
        print(f"Error reproduciendo sonido: {e}")


def ejecutar_envio_whatsapp(numero_contacto: str, mensaje: str) -> None:

    mensaje_completo = mensaje 
    # -------------------

    texto = urllib.parse.quote(mensaje_completo)
    url = f"https://wa.me/{numero_contacto}?text={texto}"
    
    # 1. Abrir navegador
    webbrowser.open(url)

    if pyautogui is None:
        print("Falta pyautogui. Enviar manual.")
        return

    time.sleep(10)  

    try:
        pyautogui.press('enter') 
        time.sleep(1)
        pyautogui.press('enter') 
        time.sleep(2) 
        
    except Exception as e:
        print(f"Error automatizando: {e}")
