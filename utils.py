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

def reproducir_sonido_exito():
    """Reproduce el archivo de sonido checklist_ok.wav."""
    try:
        # Reproducir archivo WAV de forma asíncrona
        winsound.PlaySound("checklist_ok.wav", winsound.SND_FILENAME | winsound.SND_ASYNC)
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
