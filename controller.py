"""
controller.py
"""
from typing import List, Dict
from models import TareaBase, Medicamento, Seguridad
from database import GestorBaseDatos
import auth
import utils
import time
import pyttsx3
import threading
import queue
import subprocess

class AppController:
    def __init__(self):
        self.tareas: List[TareaBase] = GestorBaseDatos.cargar_todo()
        self.contactos: List[Dict[str, str]] = GestorBaseDatos.cargar_contactos()

    # --- Persistencia y Tareas (Igual) ---
    def guardar_tareas(self) -> None:
        GestorBaseDatos.guardar_todo(self.tareas)

    def cargar_tareas(self) -> List[TareaBase]:
        self.tareas = GestorBaseDatos.cargar_todo()
        return self.tareas

    def agregar_tarea_medicamento(self, nombre: str, hora: str, dosis: str, frecuencia: str) -> None:
        self.tareas.append(Medicamento(nombre, hora, dosis, frecuencia=frecuencia))
        self.guardar_tareas()

    def agregar_tarea_seguridad(self, nombre: str, hora: str, ubicacion: str, frecuencia: str) -> None:
        self.tareas.append(Seguridad(nombre, hora, ubicacion, frecuencia=frecuencia))
        self.guardar_tareas()

    def marcar_completado(self, indice: int) -> None:
        if 0 <= indice < len(self.tareas):
            self.tareas[indice].completar()
            self.guardar_tareas()

    def eliminar_tarea(self, indice: int) -> None:
        if 0 <= indice < len(self.tareas):
            self.tareas.pop(indice)
            self.guardar_tareas()

    # --- Contactos (Igual) ---
    def agregar_contacto(self, nombre: str, numero: str) -> None:
        self.contactos.append({"nombre": nombre, "numero": numero})
        GestorBaseDatos.guardar_contactos(self.contactos)

    def eliminar_contacto(self, indice: int) -> None:
        if 0 <= indice < len(self.contactos):
            self.contactos.pop(indice)
            GestorBaseDatos.guardar_contactos(self.contactos)
            
    def obtener_contactos(self) -> List[Dict[str, str]]:
        return self.contactos

    # --- Auth (Igual) ---
    def existe_contrasena(self) -> bool:
        return auth.existe_contrasena()

    def establecer_contrasena(self, password: str) -> None:
        auth.establecer_contrasena(password)

    def verificar_contrasena(self, password: str) -> bool:
        return auth.verificar_contrasena(password)

    # --- ENVÍO DE ALERTAS (MODIFICADO) ---
    def enviar_alerta_masiva(self) -> str:
        """
        Envía mensajes uno por uno. 
        Retorna un string con el estado para mostrar en la UI.
        """
        if not self.contactos:
            return "SIN_CONTACTOS"

        mensaje_base = "¡AYUDA! Necesito asistencia urgente."
        
        # El loop ahora es LENTO pero SEGURO
        for contacto in self.contactos:
            numero = contacto['numero']
            # Esta llamada ahora bloquea el hilo unos 12 segundos por contacto
            utils.ejecutar_envio_whatsapp(numero, mensaje_base)
        
        return "OK"

    def enviar_alerta_individual(self, numero: str) -> None:
        """Envío de emergencia a un número manual."""
        mensaje = "¡AYUDA! Necesito asistencia urgente (Número manual)."
        utils.ejecutar_envio_whatsapp(numero, mensaje)

    def _generar_texto_tts(self, tarea):
        if isinstance(tarea, Medicamento):
            return f"Debe tomar {tarea.nombre}, dosis {tarea.dosis}, a las {tarea.hora} horas."
        elif isinstance(tarea, Seguridad):
            return f"{tarea.nombre}, en {tarea.ubicacion}, a las {tarea.hora} horas."
        else:
            return f"{tarea.nombre}, a las {tarea.hora} horas."

    def hablar_tarea(self, tarea):
        texto = self._generar_texto_tts(tarea)
        threading.Thread(target=self._sapi_tts, args=(texto,), daemon=True).start()

    def _sapi_tts(self, texto):
        comando = f'powershell -Command "Add-Type –AssemblyName System.Speech; ' \
                  f'$speak = New-Object System.Speech.Synthesis.SpeechSynthesizer; ' \
                  f'$speak.Speak(\\"{texto}\\")"'
        subprocess.run(comando, shell=True)
