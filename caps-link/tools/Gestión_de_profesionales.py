import os
import requests
from datetime import datetime
from pydantic import Field


class Tools:
    def __init__(self):
        # URL interna Docker: servicio fastapi en la red de compose
        self.api_base = os.getenv("CAPS_API_BASE_URL", "http://192.168.33.246:8000")

    def listar_profesionales(self) -> str:
        """
        Lista todos los profesionales desde la API CAPS-Link.
        """
        try:
            url = f"{self.api_base}/api/profesionales"
            r = requests.get(url, timeout=15)
            r.raise_for_status()
            data = r.json()
            return f"Profesionales: {data}"
        except requests.RequestException as e:
            return f"Error al listar profesionales: {str(e)}"

    def get_profesional(
        self,
        profesional_id: int = Field(..., description="ID del profesional a consultar"),
    ) -> str:
        """
        Obtiene un profesional por ID.
        """
        try:
            url = f"{self.api_base}/api/profesionales/{profesional_id}"
            r = requests.get(url, timeout=15)
            r.raise_for_status()
            data = r.json()
            return f"Profesional {profesional_id}: {data}"
        except requests.RequestException as e:
            return f"Error al obtener profesional {profesional_id}: {str(e)}"

    def crear_profesional(
        self,
        nombre: str = Field(..., description="Nombre del profesional"),
        especialidad: str = Field(..., description="Especialidad del profesional"),
    ) -> str:
        """
        Crea un nuevo profesional.
        """
        try:
            url = f"{self.api_base}/api/profesionales"
            payload = {
                "nombre": nombre,
                "especialidad": especialidad,
            }
            r = requests.post(url, json=payload, timeout=15)
            r.raise_for_status()
            data = r.json()
            return f"Profesional creado: {data}"
        except requests.RequestException as e:
            return f"Error al crear profesional: {str(e)}"

    def eliminar_profesional(
        self,
        profesional_id: int = Field(..., description="ID del profesional a eliminar"),
    ) -> str:
        """
        Elimina un profesional por ID.
        """
        try:
            url = f"{self.api_base}/api/profesionales/{profesional_id}"
            r = requests.delete(url, timeout=15)
            r.raise_for_status()
            return f"Profesional {profesional_id} eliminado correctamente."
        except requests.RequestException as e:
            return f"Error al eliminar profesional {profesional_id}: {str(e)}"
