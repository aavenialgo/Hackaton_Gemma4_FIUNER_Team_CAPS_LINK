# CAPS-Link (WebUI)

Este módulo contiene la interfaz conversacional del proyecto CAPS-Link usando **Open WebUI** y Docker Compose.  
Desde aquí levantás el frontend, restaurás backups de la UI y conectás con el backend FastAPI (`tools_sql`).

---

## 📁 Estructura

```text
caps-link/
├── docker-compose.yml                # Stack base: solo Open WebUI
├── docker-compose-fastapi.yml        # Stack integrado: Open WebUI + FastAPI
├── modelfiles/
│   └── Modelfile.caps-link           # Prompt/sistema del modelo (si aplica)
└── README.md
```

> `tools_sql/` está en carpeta hermana (mismo nivel que `caps-link/`), no dentro de este repo/carpeta.

---

## ✅ Requisitos

- Docker + Docker Compose v2
- Puertos disponibles:
  - `3000` para WebUI
  - `8000` para FastAPI (solo modo integrado)

Verificar:
```bash
docker --version
docker compose version
```

---

## 🚀 Modos de ejecución

## 1) Modo base (solo WebUI)

Levanta únicamente Open WebUI:

```bash
docker compose up -d
```

Abrir:
- http://localhost:3000

---

## 2) Modo integrado (WebUI + FastAPI)

Levanta WebUI + API backend:

```bash
docker compose -f docker-compose-fastapi.yml up -d --build
```

Abrir:
- WebUI: http://localhost:3000
- FastAPI docs: http://localhost:8000/docs
- Health API: http://localhost:8000/health

---

## 🔗 Conexión WebUI → FastAPI (importante)

Si configurás Tools/Functions dentro de WebUI para llamar la API:

- Usar **`http://fastapi:8000`** (red interna Docker) ✅
- No usar `http://localhost:8000` desde el contenedor webui ❌

Ejemplo endpoint:
- `GET http://fastapi:8000/api/profesionales`

---

## 💾 Persistencia y backup de WebUI

Los datos de Open WebUI se guardan en volumen Docker (ejemplo: `caps-link_open_webui_data`).

### Ver volúmenes
```bash
docker volume ls
```

### Backup
```bash
docker run --rm \
  -v caps-link_open_webui_data:/volume \
  -v ${PWD}:/backup \
  alpine sh -c "cd /volume && tar czf /backup/open_webui_data_backup.tar.gz ."
```

### Restore
```bash
docker run --rm \
  -v caps-link_open_webui_data:/volume \
  -v ${PWD}:/backup \
  alpine sh -c "cd /volume && tar xzf /backup/open_webui_data_backup.tar.gz"
```

Reiniciar:
```bash
docker compose restart
```

> ⚠️ No usar `docker compose down -v` si querés conservar datos.

---

## 🧪 Comandos útiles

Estado:
```bash
docker compose ps
docker ps
```

Logs:
```bash
docker compose logs -f
docker compose -f docker-compose-fastapi.yml logs -f
```

Bajar servicios:
```bash
docker compose down
docker compose -f docker-compose-fastapi.yml down
```

Reconstruir:
```bash
docker compose -f docker-compose-fastapi.yml up -d --build
```

---

## 🛠️ Troubleshooting

### Error: `no configuration file provided: not found`
Ejecutaste el comando fuera de `caps-link/`.  
Solución: entrar a la carpeta o usar `-f` con ruta completa al compose.

### Error: `.env not found` en modo FastAPI
Revisar ruta en `docker-compose-fastapi.yml` hacia `tools_sql/.env`  
(según tu estructura de carpetas hermana).

### WebUI no llega a FastAPI
1. Verificar ambos contenedores arriba (`docker ps`)  
2. Probar desde webui:
```bash
docker exec -it caps-link-webui sh
wget -qO- http://fastapi:8000/health
```

---

## 📌 Estado

- [x] Open WebUI funcionando en Docker
- [x] Persistencia por volumen
- [x] Compose integrado con FastAPI
- [x] Base lista para Tools clínicas (pacientes/profesionales/consultas)

---

## 🔄 Relación con otros módulos

Este README cubre **solo `caps-link/`**.  
Para backend/API ver: `../tools_sql/README.md`  
Para visión completa del proyecto ver: `../README.md`


## 🧩 Extensiones clínicas (Tools + Prompts)

Este proyecto incluye configuración para extender Open WebUI con:

- **Tools Python**: funciones que conectan con la API FastAPI (`tools_sql`) para operar sobre base de datos clínica.
- **Prompts de sistema**: comportamientos predefinidos por módulo (SOAP, Admisión, Farmacia).

### Estructura sugerida

```text
caps-link/
├── tools/
│   ├── gestion_de_paciente.py
│   ├── gestion_de_profesionales.py
│   ├── gestion_de_consulta.py
│   └── README.md
└── prompts/
    ├── prompt_system_workspace_consulta.md
    ├── prompt_system_workspace_admision.md
    └── README.md
├── habilidades
    ├── validacion_datos_minimos.md
```

### 1) Tools (conexión a FastAPI)

Las tools deben usar como base URL interna Docker:

- `http://fastapi:8000`

Ejemplos de operaciones:
- `GET /api/profesionales`
- `POST /api/pacientes`
- `POST /api/consultas`

### 2) Prompts por módulo clínico

Perfiles de comportamiento para asistentes, por ejemplo:

- **CAPS - Módulo de Consulta Médica (SOAP)**  
  Estructura notas clínicas en formato SOAP.
- **CAPS - Módulo de Admisión**  
  Registro administrativo y triaje inicial.
- **CAPS - Gestión de Farmacia**  
  Gestión de lotes, stock y vencimientos.

> Recomendación: versionar estos prompts en `prompts/*.md` y mantener un changelog breve por cada módulo.