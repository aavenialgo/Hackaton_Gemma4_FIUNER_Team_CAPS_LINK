from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from .db import Base, engine, get_db
from . import models, schemas, crud

Base.metadata.create_all(bind=engine)

app = FastAPI(title="CAPS-Link API", version="0.1.0")

@app.get("/")
def root():
    return {"message": "CAPS-Link API running"}

@app.get("/health")
def health():
    return {"ok": True}


@app.post("/api/profesionales", response_model=schemas.ProfesionalOut)
def crear_profesional(payload: schemas.ProfesionalCreate, db: Session = Depends(get_db)):
    existente = db.query(models.Profesional).filter(models.Profesional.matricula == payload.matricula).first()
    if existente:
        raise HTTPException(status_code=409, detail="Ya existe un profesional con esa matrícula")
    return crud.crear_profesional(db, payload)

@app.get("/api/profesionales", response_model=list[schemas.ProfesionalOut])
def listar_profesionales(db: Session = Depends(get_db)):
    return db.query(models.Profesional).all()


@app.get("/api/profesionales/{profesional_id}", response_model=schemas.ProfesionalOut)
def get_profesional(profesional_id: int, db: Session = Depends(get_db)):
    profesional = db.query(models.Profesional).filter(models.Profesional.id == profesional_id).first()
    if not profesional:
        raise HTTPException(status_code=404, detail="Profesional no encontrado")
    return profesional

@app.post("/api/pacientes", response_model=schemas.PacienteOut)
def crear_paciente(payload: schemas.PacienteCreate, db: Session = Depends(get_db)):
    existente = crud.buscar_paciente_por_dni(db, payload.dni)
    if existente:
        raise HTTPException(status_code=409, detail="Paciente ya existe")
    return crud.crear_paciente(db, payload)


@app.get("/api/pacientes/{dni}", response_model=schemas.PacienteOut)
def get_paciente(dni: str, db: Session = Depends(get_db)):
    paciente = crud.buscar_paciente_por_dni(db, dni)
    if not paciente:
        raise HTTPException(status_code=404, detail="Paciente no encontrado")
    return paciente


@app.patch("/api/pacientes/{dni}", response_model=schemas.PacienteOut)
def actualizar_paciente(dni: str, payload: schemas.PacienteUpdate, db: Session = Depends(get_db)):
    paciente = crud.buscar_paciente_por_dni(db, dni)
    if not paciente:
        raise HTTPException(status_code=404, detail="Paciente no encontrado")

    datos_actualizados = payload.model_dump(exclude_unset=True)
    if not datos_actualizados:
        raise HTTPException(status_code=400, detail="No se proporcionaron datos para actualizar")

    for campo, valor in datos_actualizados.items():
        setattr(paciente, campo, valor)

    db.commit()
    db.refresh(paciente)
    return paciente


@app.post("/api/consultas", response_model=schemas.ConsultaOut)
def crear_consulta(payload: schemas.ConsultaCreate, db: Session = Depends(get_db)):
    paciente = db.query(models.Paciente).filter(models.Paciente.id == payload.paciente_id).first()
    if not paciente:
        raise HTTPException(status_code=404, detail="Paciente no existe")
    return crud.crear_consulta(db, payload)


@app.get("/api/consultas/{consulta_id}", response_model=schemas.ConsultaOut)
def get_consulta(consulta_id: int, db: Session = Depends(get_db)):
    consulta = crud.obtener_consulta(db, consulta_id)
    if not consulta:
        raise HTTPException(status_code=404, detail="Consulta no encontrada")
    return consulta


@app.get("/api/pacientes/{dni}/consultas", response_model=schemas.PacienteConConsultas)
def get_consultas_de_paciente(dni: str, db: Session = Depends(get_db)):
    paciente = crud.buscar_paciente_por_dni(db, dni)
    if not paciente:
        raise HTTPException(status_code=404, detail="Paciente no encontrado")
    consultas = crud.listar_consultas_por_paciente(db, paciente.id)
    return {"paciente": paciente, "consultas": consultas}

@app.delete("/api/profesionales/{profesional_id}", status_code=204)
def eliminar_profesional(profesional_id: int, db: Session = Depends(get_db)):
    profesional = db.query(models.Profesional).filter(models.Profesional.id == profesional_id).first()
    if not profesional:
        raise HTTPException(status_code=404, detail="Profesional no encontrado")

    db.delete(profesional)
    db.commit()
    return None


@app.delete("/api/consultas/{consulta_id}", status_code=204)
def eliminar_consulta(consulta_id: int, db: Session = Depends(get_db)):
    consulta = crud.obtener_consulta(db, consulta_id)
    if not consulta:
        raise HTTPException(status_code=404, detail="Consulta no encontrada")

    db.delete(consulta)
    db.commit()
    return None


