"""
controller.py

Controlador que conecta la Vista (UI) con los Modelos y la persistencia.
Contiene la lógica de negocio: cargar/guardar tareas, agregar, completar, y
operaciones de autenticación y envío de alertas.
"""

from typing import List
from models import TareaBase, Medicamento, Seguridad
from database import GestorBaseDatos
import auth
import utils


class AppController:
    """
    Controlador principal de la aplicación.
    """

    def __init__(self):
        # Cargar tareas desde la "base de datos"
        self.tareas: List[TareaBase] = GestorBaseDatos.cargar_todo()

    # ----- Persistencia -----
    def guardar_tareas(self) -> None:
        """Guarda la lista actual de tareas en persistencia."""
        GestorBaseDatos.guardar_todo(self.tareas)

    def cargar_tareas(self) -> List[TareaBase]:
        """Recarga tareas desde persistencia y las retorna."""
        self.tareas = GestorBaseDatos.cargar_todo()
        return self.tareas

    # ----- Operaciones sobre tareas -----
    def agregar_tarea_medicamento(self, nombre: str, hora: str, dosis: str) -> None:
        """Agrega una tarea tipo Medicamento."""
        self.tareas.append(Medicamento(nombre, hora, dosis))
        self.guardar_tareas()

    def agregar_tarea_seguridad(self, nombre: str, hora: str, ubicacion: str) -> None:
        """Agrega una tarea tipo Seguridad."""
        self.tareas.append(Seguridad(nombre, hora, ubicacion))
        self.guardar_tareas()

    def marcar_completado(self, indice: int) -> None:
        """Marca la tarea en el índice dado como completada y guarda cambios."""
        if 0 <= indice < len(self.tareas):
            self.tareas[indice].completar()
            self.guardar_tareas()

    # ----- Autenticación -----
    def existe_contrasena(self) -> bool:
        """Retorna True si ya se estableció una contraseña admin."""
        return auth.existe_contrasena()

    def establecer_contrasena(self, password: str) -> None:
        """Establece la contraseña admin (solo primera vez)."""
        auth.establecer_contrasena(password)

    def verificar_contrasena(self, password: str) -> bool:
        """Verifica la contraseña admin."""
        return auth.verificar_contrasena(password)

    # ----- Envío de alertas -----
    def enviar_alerta_familia(self, numero_contacto: str, mensaje: str) -> None:
        """
        Inicia el proceso de envío de alerta. Ejecuta la función util en hilo.
        Args:
            numero_contacto (str): Número destino en formato internacional sin '+'.
            mensaje (str): Mensaje a enviar.
        """
        # Ejecutamos la función que abre WhatsApp Web (internamente maneja threading si aplica)
        utils.ejecutar_envio_whatsapp(numero_contacto, mensaje)
