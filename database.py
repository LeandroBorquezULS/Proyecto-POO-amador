"""
database.py

Responsable de persistencia de tareas en CSV.
No incluye tareas por defecto: si el archivo no existe, se devuelve lista vacía.
"""

import csv
import os
from typing import List

from models import TareaBase, Medicamento, Seguridad


class GestorBaseDatos:
    """
    Clase de acceso a la "base de datos" (CSV simple).

    Uso:
        GestorBaseDatos.ARCHIVO = 'ruta_si_deseas.csv'
        GestorBaseDatos.guardar_todo(lista_tareas)
        tareas = GestorBaseDatos.cargar_todo()
    """

    ARCHIVO = "agenda_amador.csv"

    @classmethod
    def guardar_todo(cls, lista_tareas: List[TareaBase]) -> None:
        """
        Guarda todas las tareas en formato CSV.

        Args:
            lista_tareas (List[TareaBase]): Lista de objetos tarea.
        """
        try:
            with open(cls.ARCHIVO, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(["Tipo", "Nombre", "Hora", "Extra", "Estado"])
                for t in lista_tareas:
                    writer.writerow(t.to_csv_row())
        except IOError as e:
            # No usamos messagebox aquí (capa UI) — lanzamos excepción para que el controlador la maneje.
            raise

    @classmethod
    def cargar_todo(cls) -> List[TareaBase]:
        """
        Carga tareas desde CSV.

        Returns:
            List[TareaBase]: Lista de tareas (vacía si no existe archivo o está vacío).
        """
        tareas = []
        if not os.path.exists(cls.ARCHIVO):
            return tareas  # Empezar sin tareas predefinidas

        try:
            with open(cls.ARCHIVO, 'r', encoding='utf-8') as f:
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
            # En caso de error devolvemos lista vacía (controlador puede loggear/mostrar error)
            return []
