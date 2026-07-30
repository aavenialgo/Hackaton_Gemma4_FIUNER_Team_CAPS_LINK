import os
import requests
from pydantic import BaseModel, Field
from pydantic.fields import FieldInfo


class Tools:
    def __init__(self):
        # Apunta al host de Docker o a la IP donde corre tu FastAPI
        self.api_base = os.getenv("CAPS_API_BASE_URL", "http://192.168.33.246:8000")

    def _clean(self, value):
        """Sanitiza campos omitidos por el LLM para evitar errores de serialización."""
        if isinstance(value, FieldInfo):
            value = value.default if value.default is not ... else None
        return value if value != "" else None

    def crear_consulta_soap(
        self,
        paciente_id: int = Field(
            ..., description="ID numérico del paciente obtenido del sistema local."
        ),
        profesional_id: int = Field(
            ..., description="ID numérico del profesional de salud que atiende."
        ),
        motivo_consulta: str = Field(
            ..., description="Motivo principal de la consulta expresado de forma breve."
        ),
        soap_subjetivo: str = Field(
            ..., description="Apartado S (Subjetivo): Síntomas y relato del paciente."
        ),
        soap_objetivo: str = Field(
            ...,
            description="Apartado O (Objetivo): Signos vitales y hallazgos del examen físico.",
        ),
        soap_analisis: str = Field(
            ..., description="Apartado A (Análisis): Diagnóstico presuntivo."
        ),
        soap_plan: str = Field(
            ...,
            description="Apartado P (Plan): Tratamiento, medicamentos recetados y derivaciones.",
        ),
    ) -> str:
        """
        Procesa, estructura y guarda el registro clínico SOAP en la base de datos local del CAPS.
        Úsalo cuando finalice la atención del paciente.
        """
        try:
            url = f"{self.api_base}/api/consultas"

            payload = {
                "paciente_id": self._clean(paciente_id),
                "profesional_id": self._clean(profesional_id),
                "motivo_consulta": self._clean(motivo_consulta),
                "soap_subjetivo": self._clean(soap_subjetivo),
                "soap_objetivo": self._clean(soap_objetivo),
                "soap_analisis": self._clean(soap_analisis),
                "soap_plan": self._clean(soap_plan),
            }

            r = requests.post(url, json=payload, timeout=20)
            r.raise_for_status()

            datos_respuesta = r.json()
            return f"Consulta guardada exitosamente en la base de datos local. ID de consulta: {datos_respuesta.get('id', 'N/A')}"

        except requests.RequestException as e:
            detail = ""
            if hasattr(e, "response") and e.response is not None:
                detail = f" | detalle API: {e.response.text}"
            return f"Error crítico al guardar la consulta SOAP: {str(e)}{detail}"

    def obtener_historial_consultas(
        self,
        dni: str = Field(
            ..., description="DNI del paciente para buscar su historial clínico."
        ),
    ) -> str:
        """
        Recupera el historial de consultas previas de un paciente usando su DNI.
        Úsalo ANTES de crear una nueva consulta para conocer los antecedentes médicos.
        """
        try:
            # Conecta con el endpoint GET /api/pacientes/{dni}/consultas
            url = f"{self.api_base}/api/pacientes/{self._clean(dni)}/consultas"
            r = requests.get(url, timeout=20)

            if r.status_code == 404:
                return f"No se encontraron consultas previas para el DNI {dni}."

            r.raise_for_status()
            return f"Historial de consultas recuperado: {r.json()}"

        except requests.RequestException as e:
            detail = ""
            if hasattr(e, "response") and e.response is not None:
                detail = f" | detalle API: {e.response.text}"
            return f"Error al obtener el historial de consultas para el DNI {dni}: {str(e)}{detail}"
