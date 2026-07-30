from sqlalchemy import Column, Integer, String, Date, Text, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from .db import Base


class Profesional(Base):
    __tablename__ = "profesionales"

    id = Column(Integer, primary_key=True, index=True)
    nombre_completo = Column(String(150), nullable=False)
    matricula = Column(String(50), unique=True, nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    consultas = relationship("ConsultaSOAP", back_populates="profesional")


class Paciente(Base):
    __tablename__ = "pacientes"

    id = Column(Integer, primary_key=True, index=True)
    dni = Column(String(20), unique=True, index=True, nullable=False)
    nombre_completo = Column(String(150), nullable=False)
    fecha_nacimiento = Column(Date, nullable=True)
    domicilio = Column(String(250), nullable=True)
    telefono = Column(String(50), nullable=True)
    cobertura_medica = Column(String(100), nullable=True)
    antecedentes_alergias = Column(Text, nullable=True)
    medicamentos_cronicos = Column(Text, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    consultas = relationship("ConsultaSOAP", back_populates="paciente", cascade="all, delete-orphan")


class ConsultaSOAP(Base):
    __tablename__ = "consultas_soap"

    id = Column(Integer, primary_key=True, index=True)
    paciente_id = Column(Integer, ForeignKey("pacientes.id", ondelete="CASCADE"), nullable=False, index=True)
    profesional_id = Column(Integer, ForeignKey("profesionales.id", ondelete="SET NULL"), nullable=True, index=True)

    fecha_hora = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    motivo_consulta = Column(Text, nullable=False)

    soap_subjetivo = Column(Text, nullable=True)
    soap_objetivo = Column(Text, nullable=True)
    soap_analisis = Column(Text, nullable=True)
    soap_plan = Column(Text, nullable=True)

    estado_validacion = Column(String(50), default="PENDIENTE DE REVISION MEDICA", nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    paciente = relationship("Paciente", back_populates="consultas")
    profesional = relationship("Profesional", back_populates="consultas")