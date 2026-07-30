# tools_sql (FastAPI Backend)

Backend clínico de CAPS-Link desarrollado con **FastAPI**.  
Expone endpoints REST para gestionar:

- **Profesionales**
- **Pacientes**
- **Consultas**

Este servicio está pensado para ser consumido por `caps-link` (Open WebUI) vía red Docker interna.

---

## 📁 Estructura

```text
tools_sql/
├── .venv/                # Entorno virtual local (opcional para desarrollo)
├── app/                  # Código fuente FastAPI
├── data/                 # Persistencia local (sqlite u otros archivos)
├── pruebas/              # Scripts/tests de prueba
├── .dockerignore
├── .env                  # Variables de entorno
├── Dockerfile
├── requirements.txt
└── README.md
```

---

## ✅ Requisitos

### Opción A: Docker (recomendado)
- Docker + Docker Compose v2

### Opción B: Local (sin Docker)
- Python 3.10+ (o versión compatible con tu proyecto)
- pip

---

## ⚙️ Variables de entorno

Archivo `.env` (ejemplo mínimo):

```env
DATABASE_URL=sqlite:///./data/app.db
```

> Si tu app usa más variables (CORS, entorno, etc.), agrégalas aquí.

---

## 🚀 Ejecutar con Docker (solo FastAPI)

Desde `tools_sql/`:

```bash
docker build -t caps-link-fastapi .
docker run --name caps-link-fastapi -p 8000:8000 --env-file .env caps-link-fastapi
```

Accesos:
- API root: http://localhost:8000/
- Health: http://localhost:8000/health
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

---

## 🚀 Ejecutar local (sin Docker)

Desde `tools_sql/`:

```bash
python -m venv .venv
```

### Windows (PowerShell)
```powershell
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Linux/Mac
```bash
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

---

## 📚 Endpoints principales

## Profesionales
- `GET    /api/profesionales` → listar
- `POST   /api/profesionales` → crear
- `GET    /api/profesionales/{profesional_id}` → obtener por ID
- `DELETE /api/profesionales/{profesional_id}` → eliminar

## Pacientes
- `POST  /api/pacientes` → crear
- `GET   /api/pacientes/{dni}` → obtener por DNI
- `PATCH /api/pacientes/{dni}` → actualizar

### Ejemplo body `POST /api/pacientes`
```json
{
  "dni": "30111222",
  "nombre_completo": "Juan Pérez",
  "fecha_nacimiento": "1990-05-20",
  "domicilio": "Calle 123",
  "telefono": "1122334455",
  "cobertura_medica": "OSDE",
  "antecedentes_alergias": "Penicilina",
  "medicamentos_cronicos": "Ninguno"
}
```

## Consultas
- `POST   /api/consultas` → crear
- `GET    /api/consultas/{consulta_id}` → obtener por ID
- `DELETE /api/consultas/{consulta_id}` → eliminar
- `GET    /api/pacientes/{dni}/consultas` → listar consultas de un paciente

---

## 🔗 Integración con Open WebUI

Cuando `tools_sql` corre junto a `caps-link` en Docker Compose:

- URL interna recomendada para tools de WebUI:
  - `http://fastapi:8000` (si el servicio se llama `fastapi`)

Ejemplo:
- `GET http://fastapi:8000/api/profesionales`

> Desde **dentro del contenedor de WebUI**, no usar `localhost:8000`.

---

## 🧪 Testing / pruebas

Si usás carpeta `pruebas/`, podés documentar aquí tus scripts específicos.  
Ejemplo general:

```bash
python pruebas/test_basico.py
```

*(ajustar según tus archivos reales de prueba)*

---

## 🛠️ Troubleshooting

### `422 Unprocessable Entity`
El JSON enviado no coincide con el schema esperado por el endpoint.  
Revisar en `/docs` los campos requeridos y tipos.

### `Connection refused`
La API no está levantada o el puerto no está expuesto.  
Verificar:
```bash
docker ps
```

### Error de DB / ruta de archivo
Revisar `DATABASE_URL` en `.env` y que exista la carpeta `data/`.

---

## 📌 Notas de desarrollo

- FastAPI valida automáticamente con Pydantic.
- Swagger (`/docs`) es la fuente de verdad para request/response schemas.
- Mantener consistencia entre modelos, rutas y tools que consume WebUI.

---

## 🔄 Relación con otros módulos

- Frontend conversacional: `../caps-link/README.md`
- Visión general del proyecto: `../README.md`