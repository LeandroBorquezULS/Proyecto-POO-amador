"""
models.py

Modelos de datos para la aplicación (TareaBase, Medicamento, Seguridad).
"""

from typing import List


class TareaBase:
    """
    Clase base para una tarea.

    Atributos:
        nombre (str): Nombre/descripcion de la tarea.
        hora (str): Hora asociada a la tarea (texto).
        estado (str): "Pendiente" o "Completado".
    """

    def __init__(self, nombre: str, hora: str, estado: str = "Pendiente"):
        self.nombre = nombre
        self.hora = hora
        self.estado = estado

    def completar(self) -> None:
        """Marca la tarea como completada."""
        self.estado = "Completado"

    def get_descripcion_visual(self) -> str:
        """Devuelve la representación visual de la tarea para la UI."""
        return f"{self.hora} - {self.nombre}"

    def to_csv_row(self) -> List[str]:
        """Serializa la tarea a una fila lista para CSV."""
        return ["General", self.nombre, self.hora, "", self.estado]


class Medicamento(TareaBase):
    """
    Tarea tipo Medicamento.

    Atributos adicionales:
        dosis (str): Descripción de la dosis/extra.
    """

    def __init__(self, nombre: str, hora: str, dosis: str, estado: str = "Pendiente"):
        super().__init__(nombre, hora, estado)
        self.dosis = dosis

    def get_descripcion_visual(self) -> str:
        """Representación visual con icono y dosis."""
        return f"💊 {self.hora} hrs: {self.nombre} ({self.dosis})"

    def to_csv_row(self) -> List[str]:
        """Serializa la tarea tipo Medicamento para CSV."""
        return ["Medicamento", self.nombre, self.hora, self.dosis, self.estado]


class Seguridad(TareaBase):
    """
    Tarea tipo Seguridad.

    Atributos adicionales:
        ubicacion (str): Lugar relacionado a la tarea de seguridad.
    """

    def __init__(self, nombre: str, hora: str, ubicacion: str, estado: str = "Pendiente"):
        super().__init__(nombre, hora, estado)
        self.ubicacion = ubicacion

    def get_descripcion_visual(self) -> str:
        """Representación visual con icono y ubicación."""
        return f"🔒 {self.hora} hrs: {self.nombre} en {self.ubicacion}"

    def to_csv_row(self) -> List[str]:
        """Serializa la tarea tipo Seguridad para CSV."""
        return ["Seguridad", self.nombre, self.hora, self.ubicacion, self.estado]
