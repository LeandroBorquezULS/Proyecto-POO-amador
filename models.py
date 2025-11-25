"""
models.py
"""
from typing import List

class TareaBase:
    def __init__(self, nombre: str, hora: str, estado: str = "Pendiente", frecuencia: str = "Diaria"):
        self.nombre = nombre
        self.hora = hora
        self.estado = estado
        self.frecuencia = frecuencia  # Nuevo campo: "Diaria" o "Única"

    def completar(self) -> None:
        self.estado = "Completado"

    def get_descripcion_visual(self) -> str:
        # Agregamos una pequeña marca visual si es única
        tag = "[1 vez]" if self.frecuencia == "Única" else "∞"
        return f"{self.hora} - {self.nombre} {tag}"

    def to_csv_row(self) -> List[str]:
        # Agregamos frecuencia al final
        return ["General", self.nombre, self.hora, "", self.estado, self.frecuencia]


class Medicamento(TareaBase):
    def __init__(self, nombre: str, hora: str, dosis: str, estado: str = "Pendiente", frecuencia: str = "Diaria"):
        super().__init__(nombre, hora, estado, frecuencia)
        self.dosis = dosis

    def get_descripcion_visual(self) -> str:
        tag = "[1 vez]" if self.frecuencia == "Única" else "∞"
        return f"💊 {self.hora} hrs: {self.nombre} ({self.dosis}) {tag}"

    def to_csv_row(self) -> List[str]:
        return ["Medicamento", self.nombre, self.hora, self.dosis, self.estado, self.frecuencia]


class Seguridad(TareaBase):
    def __init__(self, nombre: str, hora: str, ubicacion: str, estado: str = "Pendiente", frecuencia: str = "Diaria"):
        super().__init__(nombre, hora, estado, frecuencia)
        self.ubicacion = ubicacion

    def get_descripcion_visual(self) -> str:
        tag = "[1 vez]" if self.frecuencia == "Única" else "∞"
        return f"🔒 {self.hora} hrs: {self.nombre} en {self.ubicacion} {tag}"

    def to_csv_row(self) -> List[str]:
        return ["Seguridad", self.nombre, self.hora, self.ubicacion, self.estado, self.frecuencia]
