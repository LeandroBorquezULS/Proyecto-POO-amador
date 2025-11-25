"""
utils.py
"""
import time
import webbrowser
import urllib.parse
# threading ya no se usa aqui dentro, lo maneja el controller

try:
    import pyautogui
except ImportError:
    pyautogui = None

# --- TU UBICACIÓN FIJA (Recuerda poner tu link real aqui) ---
LINK_CASA = "https://www.google.com/maps/place/La+Serena,+Coquimbo" 

def ejecutar_envio_whatsapp(numero_contacto: str, mensaje: str) -> None:
    """
    Abre WhatsApp, espera y presiona Enter.
    Es una función SINCRÓNICA (el código se detiene aquí hasta terminar).
    """
    mensaje_completo = f"{mensaje} Ubicación: {LINK_CASA}"
    texto = urllib.parse.quote(mensaje_completo)
    url = f"https://wa.me/{numero_contacto}?text={texto}"
    
    # 1. Abrir navegador
    webbrowser.open(url)

    # Si no hay pyautogui, no podemos hacer más
    if pyautogui is None:
        print("Falta pyautogui. Enviar manual.")
        return

    # 2. ESPERA CRÍTICA: Damos 10 segundos para que cargue WhatsApp Web y el chat.
    # Si tu PC es lento, sube esto a 15.
    time.sleep(10)  

    try:
        # 3. Asegurar foco (Clic al medio por si acaso) y enviar
        # width, height = pyautogui.size()
        # pyautogui.click(width / 2, height / 2) # Opcional: hacer clic en el centro
        
        pyautogui.press('enter') # Primer enter para entrar al chat si sale popup
        time.sleep(1)
        pyautogui.press('enter') # Segundo enter para enviar mensaje
        
        # Esperamos un poco para asegurar que el mensaje salga antes de cerrar o cambiar
        time.sleep(2) 
        
    except Exception as e:
        print(f"Error automatizando: {e}")
