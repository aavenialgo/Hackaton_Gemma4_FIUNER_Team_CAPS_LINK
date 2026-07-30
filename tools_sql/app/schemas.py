from datetime import date, datetime
from typing import Optional, List
from pydantic import BaseModel


class ProfesionalCreate(BaseModel):
    nombre_completo: str
    matricula: str


class ProfesionalOut(BaseModel):
    id: int
    nombre_completo: str
    matricula: str

    class Config:
        from_attributes = True


class PacienteCreate(BaseModel):
    dni: str
    nombre_completo: str
    fecha_nacimiento: Optional[date] = None
    domicilio: Optional[str] = None
    telefono: Optional[str] = None
    cobertura_medica: Optional[str] = None
    antecedentes_alergias: Optional[str] = None
    medicamentos_cronicos: Optional[str] = None


class PacienteUpdate(BaseModel):
    nombre_completo: Optional[str] = None
    fecha_nacimiento: Optional[date] = None
    domicilio: Optional[str] = None
    telefono: Optional[str] = None
    cobertura_medica: Optional[str] = None
    antecedentes_alergias: Optional[str] = None
    medicamentos_cronicos: Optional[str] = None


class PacienteOut(PacienteCreate):
    id: int

    class Config:
        from_attributes = True


class ConsultaCreate(BaseModel):
    paciente_id: int
    motivo_consulta: str


class ConsultaUpdate(BaseModel):
    soap_subjetivo: Optional[str] = None
    soap_objetivo: Optional[str] = None
    soap_analisis: Optional[str] = None
    soap_plan: Optional[str] = None
    profesional_id: Optional[int] = None
    estado_validacion: Optional[str] = None


class ConsultaOut(BaseModel):
    id: int
    paciente_id: int
    profesional_id: Optional[int]
    fecha_hora: datetime
    motivo_consulta: str
    soap_subjetivo: Optional[str]
    soap_objetivo: Optional[str]
    soap_analisis: Optional[str]
    soap_plan: Optional[str]
    estado_validacion: str

    class Config:
        from_attributes = True


class PacienteConConsultas(BaseModel):
    paciente: PacienteOut
    consultas: List[ConsultaOut]