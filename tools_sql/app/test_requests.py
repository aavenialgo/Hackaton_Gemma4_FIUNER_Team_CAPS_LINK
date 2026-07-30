import requests

BASE_URL = "http://127.0.0.1:8000"

def test_health():
    r = requests.get(f"{BASE_URL}/health")
    print("GET /health:", r.status_code, r.json())

def test_crear_profesional():
    r = requests.post(
        f"{BASE_URL}/api/profesionales",
        json={
            "nombre_completo": "Dr. Juan Pérez",
            "matricula": "MAT-001"
        }
    )
    print("POST /api/profesionales:", r.status_code, r.json())

def test_crear_paciente():
    r = requests.post(
        f"{BASE_URL}/api/pacientes",
        json={
            "dni": "12345678",
            "nombre_completo": "Ana Gómez",
            "fecha_nacimiento": "1990-01-15",
            "domicilio": "Av. Siempre Viva 123",
            "telefono": "1122334455",
            "cobertura_medica": "OSDE",
            "antecedentes_alergias": "Penicilina",
            "medicamentos_cronicos": "Insulina"
        }
    )
    print("POST /api/pacientes:", r.status_code, r.json())

def test_crear_consulta():
    r = requests.post(
        f"{BASE_URL}/api/consultas",
        json={
            "paciente_id": 1,
            "motivo_consulta": "Dolor de espalda"
        }
    )
    print("POST /api/consultas:", r.status_code, r.json())

def test_get_paciente():
    r = requests.get(f"{BASE_URL}/api/pacientes/12345678")
    print("GET /api/pacientes/{dni}:", r.status_code, r.json())

def test_get_consultas():
    r = requests.get(f"{BASE_URL}/api/pacientes/12345678/consultas")
    print("GET /api/pacientes/{dni}/consultas:", r.status_code, r.json())

if __name__ == "__main__":
    test_health()
    test_crear_profesional()
    test_crear_paciente()
    test_crear_consulta()
    test_get_paciente()
    test_get_consultas()