import os
import json
import uuid
from datetime import datetime, date
from typing import List, Optional
from fastapi import FastAPI, HTTPException, status, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, field_validator

app = FastAPI(title="Gestión de Gastos API", version="1.0.0")

# Configuración del Middleware de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DATABASE_FILE = os.path.join(os.path.dirname(__file__), "database.json")

# Modelo de Pydantic para un Gasto
class Gasto(BaseModel):
    id: Optional[str] = Field(default=None, description="Identificador único del gasto")
    importe: float = Field(..., gt=0.0, description="El importe debe ser estrictamente mayor que 0")
    categoria: str = Field(..., min_length=1, description="Categoría obligatoria, no vacía")
    descripcion: str = Field(..., min_length=1, description="Descripción obligatoria, no vacía")
    fecha: str = Field(..., description="Fecha obligatoria en formato YYYY-MM-DD")

    @field_validator("fecha")
    @classmethod
    def validar_formato_fecha(cls, v: str) -> str:
        try:
            datetime.strptime(v, "%Y-%m-%d")
        except ValueError:
            raise ValueError("El formato de fecha debe ser YYYY-MM-DD")
        return v

# Funciones de persistencia de datos
def leer_gastos() -> List[dict]:
    if not os.path.exists(DATABASE_FILE):
        return []
    try:
        with open(DATABASE_FILE, "r", encoding="utf-8") as f:
            data = f.read().strip()
            if not data:
                return []
            return json.loads(data)
    except (json.JSONDecodeError, IOError):
        return []

def guardar_gastos(gastos: List[dict]) -> None:
    with open(DATABASE_FILE, "w", encoding="utf-8") as f:
        json.dump(gastos, f, indent=4, ensure_ascii=False)

def inicializar_base_de_datos() -> None:
    gastos = leer_gastos()
    if not gastos:
        gasto_ejemplo = {
            "id": str(uuid.uuid4()),
            "importe": 15.50,
            "categoria": "Oficina",
            "descripcion": "Grapadora y folios",
            "fecha": date.today().isoformat()
        }
        guardar_gastos([gasto_ejemplo])

# Inicializar base de datos al arrancar
inicializar_base_de_datos()

# Endpoints de la API
@app.post("/api/gastos", response_model=Gasto, status_code=status.HTTP_201_CREATED)
def crear_gasto(gasto: Gasto):
    if not gasto.id:
        gasto.id = str(uuid.uuid4())
    
    gastos = leer_gastos()
    # Evitar duplicaciones de ID si por casualidad ocurriera
    if any(g["id"] == gasto.id for g in gastos):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Un gasto con este ID ya existe."
        )
        
    gasto_dict = gasto.model_dump()
    gastos.append(gasto_dict)
    guardar_gastos(gastos)
    return gasto

@app.get("/api/gastos", response_model=List[Gasto])
def obtener_gastos(
    categoria: Optional[str] = Query(None, description="Filtrar por categoría"),
    fecha_inicio: Optional[str] = Query(None, description="Filtrar fecha inicial YYYY-MM-DD"),
    fecha_fin: Optional[str] = Query(None, description="Filtrar fecha final YYYY-MM-DD")
):
    gastos = leer_gastos()
    resultado = []

    # Validar formato de fechas de filtro si se pasan
    if fecha_inicio:
        try:
            datetime.strptime(fecha_inicio, "%Y-%m-%d")
        except ValueError:
            raise HTTPException(status_code=400, detail="Formato fecha_inicio incorrecto, debe ser YYYY-MM-DD")
    if fecha_fin:
        try:
            datetime.strptime(fecha_fin, "%Y-%m-%d")
        except ValueError:
            raise HTTPException(status_code=400, detail="Formato fecha_fin incorrecto, debe ser YYYY-MM-DD")

    for g in gastos:
        # Filtro de categoría (case insensitive)
        if categoria and categoria.lower() not in g["categoria"].lower():
            continue
        
        # Filtro de fecha de inicio
        if fecha_inicio and g["fecha"] < fecha_inicio:
            continue
            
        # Filtro de fecha de fin
        if fecha_fin and g["fecha"] > fecha_fin:
            continue
            
        resultado.append(g)

    return resultado

@app.put("/api/gastos/{gasto_id}", response_model=Gasto)
def actualizar_gasto(gasto_id: str, gasto_actualizado: Gasto):
    gastos = leer_gastos()
    
    for idx, g in enumerate(gastos):
        if g["id"] == gasto_id:
            # Mantener el ID original del path
            gasto_actualizado.id = gasto_id
            gastos[idx] = gasto_actualizado.model_dump()
            guardar_gastos(gastos)
            return gasto_actualizado

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, 
        detail=f"Gasto con ID {gasto_id} no encontrado."
    )

@app.delete("/api/gastos/{gasto_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_gasto(gasto_id: str):
    gastos = leer_gastos()
    
    nuevo_listado = [g for g in gastos if g["id"] != gasto_id]
    if len(nuevo_listado) == len(gastos):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Gasto con ID {gasto_id} no encontrado."
        )
        
    guardar_gastos(nuevo_listado)
    return
