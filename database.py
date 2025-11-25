"""
database.py
"""
import csv
import json
import os
from typing import List, Dict
from models import TareaBase, Medicamento, Seguridad

class GestorBaseDatos:
    ARCHIVO_TAREAS = "agenda_amador.csv"
    ARCHIVO_CONTACTOS = "contactos.json"

    @classmethod
    def guardar_todo(cls, lista_tareas: List[TareaBase]) -> None:
        try:
            with open(cls.ARCHIVO_TAREAS, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                # Agregamos "Frecuencia" al encabezado
                writer.writerow(["Tipo", "Nombre", "Hora", "Extra", "Estado", "Frecuencia"])
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
                    # Recuperamos la frecuencia, por defecto "Diaria" si no existe
                    freq = row.get("Frecuencia", "Diaria")
                    
                    if tipo == "Medicamento":
                        obj = Medicamento(row.get("Nombre", ""), row.get("Hora", ""), row.get("Extra", ""), row.get("Estado", "Pendiente"), freq)
                    elif tipo == "Seguridad":
                        obj = Seguridad(row.get("Nombre", ""), row.get("Hora", ""), row.get("Extra", ""), row.get("Estado", "Pendiente"), freq)
                    else:
                        obj = TareaBase(row.get("Nombre", ""), row.get("Hora", ""), row.get("Estado", "Pendiente"), freq)
                    tareas.append(obj)
            return tareas
        except Exception:
            return []

    # --- CONTACTOS (IGUAL QUE ANTES) ---
    @classmethod
    def guardar_contactos(cls, lista_contactos: List[Dict[str, str]]) -> None:
        try:
            with open(cls.ARCHIVO_CONTACTOS, 'w', encoding='utf-8') as f:
                json.dump(lista_contactos, f, indent=4)
        except IOError:
            raise

    @classmethod
    def cargar_contactos(cls) -> List[Dict[str, str]]:
        if not os.path.exists(cls.ARCHIVO_CONTACTOS):
            return []
        try:
            with open(cls.ARCHIVO_CONTACTOS, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            return []
