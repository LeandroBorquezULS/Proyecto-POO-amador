
from typing import List, Dict
from models import TareaBase, Medicamento, Seguridad
from database import GestorBaseDatos
import auth
import utils
import time

class AppController:
    def __init__(self):
        self.tareas: List[TareaBase] = GestorBaseDatos.cargar_todo()
        # Cargar contactos al iniciar
        self.contactos: List[Dict[str, str]] = GestorBaseDatos.cargar_contactos()

    # ----- Persistencia Tareas -----
    def guardar_tareas(self) -> None:
        GestorBaseDatos.guardar_todo(self.tareas)

    def cargar_tareas(self) -> List[TareaBase]:
        self.tareas = GestorBaseDatos.cargar_todo()
        return self.tareas

    # ----- Operaciones sobre tareas -----
    def agregar_tarea_medicamento(self, nombre: str, hora: str, dosis: str) -> None:
        self.tareas.append(Medicamento(nombre, hora, dosis))
        self.guardar_tareas()

    def agregar_tarea_seguridad(self, nombre: str, hora: str, ubicacion: str) -> None:
        self.tareas.append(Seguridad(nombre, hora, ubicacion))
        self.guardar_tareas()

    def marcar_completado(self, indice: int) -> None:
        if 0 <= indice < len(self.tareas):
            self.tareas[indice].completar()
            self.guardar_tareas()

    # ----- NUEVO: Gestión de Contactos -----
    def agregar_contacto(self, nombre: str, numero: str) -> None:
        self.contactos.append({"nombre": nombre, "numero": numero})
        GestorBaseDatos.guardar_contactos(self.contactos)

    def eliminar_contacto(self, indice: int) -> None:
        if 0 <= indice < len(self.contactos):
            self.contactos.pop(indice)
            GestorBaseDatos.guardar_contactos(self.contactos)
            
    def obtener_contactos(self) -> List[Dict[str, str]]:
        return self.contactos

    # ----- Autenticación -----
    def existe_contrasena(self) -> bool:
        return auth.existe_contrasena()

    def establecer_contrasena(self, password: str) -> None:
        auth.establecer_contrasena(password)

    def verificar_contrasena(self, password: str) -> bool:
        return auth.verificar_contrasena(password)

    # ----- Envío de alertas (MODIFICADO) -----
    def enviar_alerta_masiva(self) -> None:
        """
        Envía el mensaje de ayuda a TODOS los contactos registrados.
        """
        mensaje = "¡AYUDA! Necesito asistencia urgente en casa."
        
        if not self.contactos:
            print("No hay contactos registrados para enviar alerta.")
            return

        for contacto in self.contactos:
            numero = contacto['numero']
            # Llamamos al util. Se abrirá una pestaña nueva por cada contacto.
            utils.ejecutar_envio_whatsapp(numero, mensaje)
            # Pequeña pausa para evitar que el navegador se bloquee si son muchos
            time.sleep(1)
