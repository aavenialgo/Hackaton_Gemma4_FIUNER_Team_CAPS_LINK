import os
import requests
from pydantic import Field
from pydantic.fields import FieldInfo


class Tools:
    def __init__(self):
        # CORRECCIÓN 1: Eliminamos "/docs" del base_url. La API base apunta al host.
        self.api_base = os.getenv("CAPS_API_BASE_URL", "http://192.168.33.246:8000")

    def _clean(self, value):
        """
        CORRECCIÓN 2: Sanitizador.
        Si el LLM omite el campo, Python asigna el objeto FieldInfo. Lo interceptamos.
        """
        if isinstance(value, FieldInfo):
            # Extraemos el valor por defecto que definiste en el Field (ej. "")
            value = value.default if value.default is not ... else None

        # Convertimos los strings vacíos a None para que FastAPI los ignore correctamente
        return value if value != "" else None

    def crear_paciente(
        self,
        dni: str = Field(..., description="DNI del paciente"),
        nombre_completo: str = Field(..., description="Nombre y apellido del paciente"),
        fecha_nacimiento: str = Field("", description="Fecha YYYY-MM-DD"),
        domicilio: str = Field("", description="Domicilio"),
        telefono: str = Field("", description="Teléfono"),
        cobertura_medica: str = Field("", description="Cobertura médica"),
        antecedentes_alergias: str = Field("", description="Alergias/antecedentes"),
        medicamentos_cronicos: str = Field("", description="Medicamentos crónicos"),
    ) -> str:
        """
        Crea un paciente en la API (/api/pacientes).
        """
        try:
            url = f"{self.api_base}/api/pacientes"

            # Pasamos todas las variables por nuestro filtro sanitizador
            payload_bruto = {
                "dni": self._clean(dni),
                "nombre_completo": self._clean(nombre_completo),
                "fecha_nacimiento": self._clean(fecha_nacimiento),
                "domicilio": self._clean(domicilio),
                "telefono": self._clean(telefono),
                "cobertura_medica": self._clean(cobertura_medica),
                "antecedentes_alergias": self._clean(antecedentes_alergias),
                "medicamentos_cronicos": self._clean(medicamentos_cronicos),
            }

            # Filtramos los None para enviar un JSON limpio a tu esquema de FastAPI
            payload = {k: v for k, v in payload_bruto.items() if v is not None}

            r = requests.post(url, json=payload, timeout=20)
            r.raise_for_status()
            return f"Paciente creado exitosamente: {r.json()}"

        except requests.RequestException as e:
            detail = ""
            if hasattr(e, "response") and e.response is not None:
                detail = f" | detalle API: {e.response.text}"
            return f"Error al crear paciente: {str(e)}{detail}"

    def get_paciente(
        self,
        dni: str = Field(..., description="DNI del paciente a consultar"),
    ) -> str:
        """
        Obtiene un paciente por DNI (/api/pacientes/{dni}).
        """
        try:
            url = f"{self.api_base}/api/pacientes/{self._clean(dni)}"
            r = requests.get(url, timeout=20)

            if r.status_code == 404:
                return f"El paciente con DNI {dni} no existe en la base de datos."

            r.raise_for_status()
            return f"Paciente recuperado {dni}: {r.json()}"

        except requests.RequestException as e:
            detail = ""
            if hasattr(e, "response") and e.response is not None:
                detail = f" | detalle API: {e.response.text}"
            return f"Error al obtener paciente {dni}: {str(e)}{detail}"

    def actualizar_paciente(
        self,
        dni: str = Field(..., description="DNI del paciente a actualizar"),
        nombre_completo: str = Field("", description="Nuevo nombre completo"),
        fecha_nacimiento: str = Field("", description="Nueva fecha YYYY-MM-DD"),
        domicilio: str = Field("", description="Nuevo domicilio"),
        telefono: str = Field("", description="Nuevo teléfono"),
        cobertura_medica: str = Field("", description="Nueva cobertura médica"),
        antecedentes_alergias: str = Field(
            "", description="Nuevas alergias/antecedentes"
        ),
        medicamentos_cronicos: str = Field(
            "", description="Nuevos medicamentos crónicos"
        ),
    ) -> str:
        """
        Actualiza un paciente por DNI (/api/pacientes/{dni}) usando PATCH.
        Solo envía campos no vacíos.
        """
        try:
            url = f"{self.api_base}/api/pacientes/{self._clean(dni)}"

            payload_bruto = {
                "nombre_completo": self._clean(nombre_completo),
                "fecha_nacimiento": self._clean(fecha_nacimiento),
                "domicilio": self._clean(domicilio),
                "telefono": self._clean(telefono),
                "cobertura_medica": self._clean(cobertura_medica),
                "antecedentes_alergias": self._clean(antecedentes_alergias),
                "medicamentos_cronicos": self._clean(medicamentos_cronicos),
            }

            payload = {k: v for k, v in payload_bruto.items() if v is not None}

            if not payload:
                return "No se enviaron campos válidos para actualizar."

            r = requests.patch(url, json=payload, timeout=20)
            r.raise_for_status()
            return f"Paciente actualizado ({dni}): {r.json()}"

        except requests.RequestException as e:
            detail = ""
            if hasattr(e, "response") and e.response is not None:
                detail = f" | detalle API: {e.response.text}"
            return f"Error al actualizar paciente {dni}: {str(e)}{detail}"
