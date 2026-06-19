import os
import json
import uuid
import pytest
from datetime import date
import sys
from fastapi.testclient import TestClient
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import main as main

@pytest.fixture(autouse=True)
def setup_test_db(monkeypatch, tmp_path):
    # Usar un archivo de base de datos temporal aislado para las pruebas
    test_db = tmp_path / "database_test.json"
    monkeypatch.setattr(main, "DATABASE_FILE", str(test_db))
    # Asegurarnos de que inicie limpio
    if os.path.exists(test_db):
        os.remove(test_db)
    yield
    # Limpieza al finalizar
    if os.path.exists(test_db):
        os.remove(test_db)

@pytest.fixture
def client():
    return TestClient(main.app)

# 1. Escenarios Estándar (Happy Path)
def test_inicializacion_base_de_datos(client):
    # Ejecutar inicialización sobre la base de datos real
    main.inicializar_base_de_datos()
    
    assert os.path.exists(main.DATABASE_FILE)
    with open(main.DATABASE_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
        
    assert len(data) >= 1
    # Verificar que el gasto de ejemplo obligatorio esté presente
    gasto_obs = next((g for g in data if g["categoria"] == "Oficina"), None)
    assert gasto_obs is not None
    assert gasto_obs["importe"] == 15.50
    assert gasto_obs["descripcion"] == "Grapadora y folios"

def test_crear_gasto_exitoso(client):
    main.inicializar_base_de_datos()
    
    payload = {
        "importe": 42.50,
        "categoria": "Comida",
        "descripcion": "Almuerzo de negocios",
        "fecha": "2026-06-19"
    }
    
    response = client.post("/api/gastos", json=payload)
    assert response.status_code == 201
    
    response_data = response.json()
    assert "id" in response_data
    assert response_data["importe"] == 42.50
    assert response_data["categoria"] == "Comida"
    assert response_data["descripcion"] == "Almuerzo de negocios"
    assert response_data["fecha"] == "2026-06-19"
    
    # Verificar formato UUID
    val_id = response_data["id"]
    try:
        uuid.UUID(val_id)
    except ValueError:
        pytest.fail("El id devuelto no es un UUID válido")

def test_listar_y_filtrar_por_categoria(client):
    main.inicializar_base_de_datos()
    
    # Agregar más gastos
    gasto1 = {
        "importe": 25.0,
        "categoria": "Transporte-Test",
        "descripcion": "Taxi al aeropuerto",
        "fecha": "2026-06-19"
    }
    gasto2 = {
        "importe": 100.0,
        "categoria": "Formacion-Test",
        "descripcion": "Libro de programación",
        "fecha": "2026-06-20"
    }
    
    post_res1 = client.post("/api/gastos", json=gasto1)
    id1 = post_res1.json()["id"]
    post_res2 = client.post("/api/gastos", json=gasto2)
    id2 = post_res2.json()["id"]
    
    # Listar todos y comprobar que los nuevos gastos están incluidos
    res_all = client.get("/api/gastos")
    assert res_all.status_code == 200
    all_data = res_all.json()
    assert any(g["id"] == id1 for g in all_data)
    assert any(g["id"] == id2 for g in all_data)
    
    # Filtrar por categoría (ej: "Transporte-Test")
    res_filter = client.get("/api/gastos?categoria=Transporte-Test")
    assert res_filter.status_code == 200
    filter_data = res_filter.json()
    assert len(filter_data) >= 1
    assert all("Transporte-Test".lower() in g["categoria"].lower() for g in filter_data)
    assert any(g["id"] == id1 for g in filter_data)
    
    # Filtrar por fecha
    res_date = client.get("/api/gastos?fecha_inicio=2026-06-20&fecha_fin=2026-06-21")
    assert res_date.status_code == 200
    date_data = res_date.json()
    assert any(g["id"] == id2 for g in date_data)
    assert not any(g["id"] == id1 for g in date_data)

def test_eliminar_gasto_exitoso(client):
    main.inicializar_base_de_datos()
    
    # Crear un gasto
    payload = {
        "importe": 10.0,
        "categoria": "Café",
        "descripcion": "Café de la mañana",
        "fecha": "2026-06-19"
    }
    create_res = client.post("/api/gastos", json=payload)
    gasto_id = create_res.json()["id"]
    
    # Eliminar
    delete_res = client.delete(f"/api/gastos/{gasto_id}")
    assert delete_res.status_code == 204
    
    # Comprobar que ya no aparece al listar
    list_res = client.get("/api/gastos")
    gastos = list_res.json()
    assert not any(g["id"] == gasto_id for g in gastos)

# 2. Escenarios de Rotura y Casos Límite (Edge Cases)

def test_error_importe_invalido(client):
    main.inicializar_base_de_datos()
    
    # Importe = 0.0
    payload_cero = {
        "importe": 0.0,
        "categoria": "Viajes",
        "descripcion": "Vuelo de ida",
        "fecha": "2026-06-19"
    }
    res_cero = client.post("/api/gastos", json=payload_cero)
    assert res_cero.status_code == 422
    
    # Importe negativo
    payload_negativo = {
        "importe": -10.50,
        "categoria": "Viajes",
        "descripcion": "Vuelo de vuelta",
        "fecha": "2026-06-19"
    }
    res_negativo = client.post("/api/gastos", json=payload_negativo)
    assert res_negativo.status_code == 422

def test_rotura_tipo_de_dato_importe(client):
    main.inicializar_base_de_datos()
    
    # Enviar texto en vez de número float
    payload = {
        "importe": "veinte_euros",
        "categoria": "Suscripciones",
        "descripcion": "Servicio mensual",
        "fecha": "2026-06-19"
    }
    res = client.post("/api/gastos", json=payload)
    assert res.status_code == 422

def test_rotura_campos_vacios_obligatorios(client):
    main.inicializar_base_de_datos()
    
    # Categoría vacía
    payload_cat_vacia = {
        "importe": 15.00,
        "categoria": "",
        "descripcion": "Compra de repuestos",
        "fecha": "2026-06-19"
    }
    res_cat = client.post("/api/gastos", json=payload_cat_vacia)
    assert res_cat.status_code == 422
    
    # Descripción vacía
    payload_desc_vacia = {
        "importe": 15.00,
        "categoria": "Oficina",
        "descripcion": "",
        "fecha": "2026-06-19"
    }
    res_desc = client.post("/api/gastos", json=payload_desc_vacia)
    assert res_desc.status_code == 422

def test_eliminar_id_inexistente_o_malformado(client):
    main.inicializar_base_de_datos()
    
    # ID inexistente/inventado
    res_inexistente = client.delete("/api/gastos/id-inventado-123")
    assert res_inexistente.status_code == 404
    
    # ID malformado (vacío o no coincidente)
    res_malformado = client.delete("/api/gastos/null")
    assert res_malformado.status_code == 404
