from sqlalchemy.orm import Session
from . import models, schemas


def crear_paciente(db: Session, data: schemas.PacienteCreate):
    paciente = models.Paciente(**data.model_dump())
    db.add(paciente)
    db.commit()
    db.refresh(paciente)
    return paciente


def buscar_paciente_por_dni(db: Session, dni: str):
    return db.query(models.Paciente).filter(models.Paciente.dni == dni).first()


def crear_profesional(db: Session, data: schemas.ProfesionalCreate):
    profesional = models.Profesional(**data.model_dump())
    db.add(profesional)
    db.commit()
    db.refresh(profesional)
    return profesional


def crear_consulta(db: Session, data: schemas.ConsultaCreate):
    consulta = models.ConsultaSOAP(**data.model_dump())
    db.add(consulta)
    db.commit()
    db.refresh(consulta)
    return consulta


def obtener_consulta(db: Session, consulta_id: int):
    return db.query(models.ConsultaSOAP).filter(models.ConsultaSOAP.id == consulta_id).first()


def actualizar_consulta(db: Session, consulta, data: schemas.ConsultaUpdate):
    for k, v in data.model_dump(exclude_unset=True).items():
        setattr(consulta, k, v)
    db.commit()
    db.refresh(consulta)
    return consulta


def listar_consultas_por_paciente(db: Session, paciente_id: int):
    return (
        db.query(models.ConsultaSOAP)
        .filter(models.ConsultaSOAP.paciente_id == paciente_id)
        .order_by(models.ConsultaSOAP.fecha_hora.desc())
        .all()
    )