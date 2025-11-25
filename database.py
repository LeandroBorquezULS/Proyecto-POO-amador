
import csv
import json
import os
from typing import List, Dict
from models import TareaBase, Medicamento, Seguridad

class GestorBaseDatos:
    ARCHIVO_TAREAS = "agenda_amador.csv"
    ARCHIVO_CONTACTOS = "contactos.json" # Nuevo archivo para guardar los números

    # --- MANEJO DE TAREAS (Igual que antes) ---
    @classmethod
    def guardar_todo(cls, lista_tareas: List[TareaBase]) -> None:
        try:
            with open(cls.ARCHIVO_TAREAS, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(["Tipo", "Nombre", "Hora", "Extra", "Estado"])
                for t in lista_tareas:
                    writer.writerow(t.to_csv_row())
        except IOError:
            raise

    @classmethod
    def cargar_todo(cls) -> List[TareaBase]:
        tareas = []
        if not os.path.exists(cls.ARCHIVO_TAREAS):
            return tareas
        try:
            with open(cls.ARCHIVO_TAREAS, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    tipo = row.get("Tipo", "General")
                    if tipo == "Medicamento":
                        obj = Medicamento(row.get("Nombre", ""), row.get("Hora", ""), row.get("Extra", ""), row.get("Estado", "Pendiente"))
                    elif tipo == "Seguridad":
                        obj = Seguridad(row.get("Nombre", ""), row.get("Hora", ""), row.get("Extra", ""), row.get("Estado", "Pendiente"))
                    else:
                        obj = TareaBase(row.get("Nombre", ""), row.get("Hora", ""), row.get("Estado", "Pendiente"))
                    tareas.append(obj)
            return tareas
        except Exception:
            return []

    # --- NUEVO: MANEJO DE CONTACTOS ---
    @classmethod
    def guardar_contactos(cls, lista_contactos: List[Dict[str, str]]) -> None:
        """Guarda la lista de diccionarios de contactos en JSON."""
        try:
            with open(cls.ARCHIVO_CONTACTOS, 'w', encoding='utf-8') as f:
                json.dump(lista_contactos, f, indent=4)
        except IOError:
            raise

    @classmethod
    def cargar_contactos(cls) -> List[Dict[str, str]]:
        """Carga la lista de contactos. Retorna lista vacía si falla o no existe."""
        if not os.path.exists(cls.ARCHIVO_CONTACTOS):
            return []
        try:
            with open(cls.ARCHIVO_CONTACTOS, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            return []
