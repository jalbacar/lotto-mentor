import os
import pandas as pd
from fastapi import FastAPI, HTTPException, Query
from typing import Optional, List, Dict
from datetime import datetime
from pydantic import BaseModel
import uvicorn

class SorteoResponse(BaseModel):
    """Modelo de respuesta para un sorteo individual"""
    fecha: str
    dow_es: str
    N1: Optional[int]
    N2: Optional[int]
    N3: Optional[int]
    N4: Optional[int]
    N5: Optional[int]
    N6: Optional[int]
    C: Optional[int]
    R: Optional[int]
    Joker: str

class EstadisticasResponse(BaseModel):
    """Modelo de respuesta para estadísticas generales"""
    total_sorteos: int
    fecha_inicio: str
    fecha_fin: str
    dias_semana: Dict[str, int]

class FrecuenciaResponse(BaseModel):
    """Modelo de respuesta para frecuencia de números"""
    frecuencia: Dict[str, int]

app = FastAPI(
    title="Lotto Data API",
    description="""API REST para acceder a datos históricos de lotería española.
    
## Características

- 🎲 **Sorteos históricos** desde 2013 hasta 2025
- 📅 **Filtros por fecha** y períodos
- 📊 **Estadísticas** y frecuencias de números
- ⚡ **Respuestas rápidas** con datos optimizados
    
## Estructura de datos

Cada sorteo contiene:
- **fecha**: Fecha del sorteo (YYYY-MM-DD)
- **dow_es**: Día de la semana en español
- **N1-N6**: Números ganadores (1-49)
- **C**: Complementario (0-49)
- **R**: Reintegro (0-9)
- **Joker**: Número Joker (opcional)
    """,
    version="1.0.0",
    contact={
        "name": "Lotto Data API",
        "url": "https://github.com/tu-usuario/lotto-api",
    },
    license_info={
        "name": "MIT",
    },
)

CSV_FILE = "data/historico_clean.csv"

def check_csv_exists():
    if not os.path.exists(CSV_FILE):
        raise HTTPException(
            status_code=404, 
            detail=f"Archivo {CSV_FILE} no encontrado. Ejecute el pipeline de datos primero."
        )

check_csv_exists()

def load_data():
    check_csv_exists()
    df = pd.read_csv(CSV_FILE)
    df['fecha'] = pd.to_datetime(df['fecha'], errors='coerce')
    df = df.dropna(subset=['fecha'])
    return df

def prepare_response(df):
    """Convierte DataFrame a formato compatible con Pydantic"""
    df = df.copy()
    df['fecha'] = df['fecha'].dt.strftime('%Y-%m-%d')
    df['Joker'] = df['Joker'].fillna('').astype(str).replace('nan', '')
    for col in ['N1', 'N2', 'N3', 'N4', 'N5', 'N6', 'C', 'R']:
        df[col] = pd.to_numeric(df[col], errors='coerce').astype('Int64')
    df = df.fillna('')
    return df.to_dict(orient="records")

@app.get("/", 
         summary="Información de la API",
         description="Endpoint raíz que proporciona información básica de la API",
         tags=["General"])
def root():
    """Endpoint principal con información de la API"""
    return {
        "message": "Lotto Data API", 
        "version": "1.0.0",
        "docs": "/docs",
        "endpoints": [
            "/sorteos",
            "/sorteos/recientes", 
            "/numeros/frecuencia",
            "/estadisticas",
            "/sorteos/fecha/{fecha}"
        ]
    }

@app.get("/sorteos", 
         response_model=List[SorteoResponse],
         summary="Obtener sorteos históricos",
         description="Devuelve una lista de sorteos históricos con opción de limitar resultados",
         tags=["Sorteos"])
def get_sorteos(limit: Optional[int] = Query(100, ge=1, le=1000, description="Número máximo de sorteos a devolver (1-1000)")):
    """Obtiene sorteos históricos ordenados por fecha descendente
    
    - **limit**: Número máximo de registros (por defecto 100, máximo 1000)
    
    Retorna lista de sorteos con todos los campos disponibles.
    """
    df = load_data()
    if limit:
        df = df.head(limit)
    return prepare_response(df)

@app.get("/sorteos/recientes", 
         response_model=List[SorteoResponse],
         summary="Sorteos recientes",
         description="Obtiene sorteos de los últimos N días",
         tags=["Sorteos"])
def get_sorteos_recientes(dias: int = Query(30, ge=1, le=365, description="Número de días hacia atrás desde la fecha más reciente (1-365)")):
    """Obtiene sorteos de los últimos N días
    
    - **dias**: Número de días hacia atrás (por defecto 30, máximo 365)
    
    Calcula desde la fecha más reciente disponible en los datos.
    """
    df = load_data()
    fecha_limite = df['fecha'].max() - pd.Timedelta(days=dias)
    df_recientes = df[df['fecha'] >= fecha_limite]
    return prepare_response(df_recientes)

@app.get("/numeros/frecuencia", 
         response_model=FrecuenciaResponse,
         summary="Frecuencia de números",
         description="Calcula la frecuencia de aparición de cada número en todos los sorteos",
         tags=["Estadísticas"])
def get_frecuencia_numeros():
    """Calcula la frecuencia de aparición de cada número (1-49)
    
    Analiza todos los números ganadores (N1-N6) de todos los sorteos
    y devuelve cuántas veces ha aparecido cada número.
    
    Útil para:
    - Análisis estadístico
    - Identificar números "calientes" y "fríos"
    - Estrategias de juego
    """
    df = load_data()
    numeros = []
    for col in ['N1', 'N2', 'N3', 'N4', 'N5', 'N6']:
        numeros.extend(pd.to_numeric(df[col], errors='coerce').dropna().tolist())
    
    frecuencia = pd.Series(numeros).value_counts().sort_index().to_dict()
    # Convertir claves a string para JSON
    frecuencia_str = {str(k): v for k, v in frecuencia.items()}
    return {"frecuencia": frecuencia_str}

@app.get("/estadisticas", 
         response_model=EstadisticasResponse,
         summary="Estadísticas generales",
         description="Proporciona estadísticas generales del conjunto de datos",
         tags=["Estadísticas"])
def get_estadisticas():
    """Obtiene estadísticas generales del conjunto de datos
    
    Incluye:
    - **total_sorteos**: Número total de sorteos disponibles
    - **fecha_inicio**: Fecha del sorteo más antiguo
    - **fecha_fin**: Fecha del sorteo más reciente
    - **dias_semana**: Distribución de sorteos por día de la semana
    
    Útil para entender la cobertura y distribución de los datos.
    """
    df = load_data()
    return {
        "total_sorteos": len(df),
        "fecha_inicio": df['fecha'].min().isoformat(),
        "fecha_fin": df['fecha'].max().isoformat(),
        "dias_semana": df['dow_es'].value_counts().to_dict()
    }

@app.get("/sorteos/fecha/{fecha}", 
         response_model=SorteoResponse,
         summary="Sorteo por fecha",
         description="Obtiene el sorteo de una fecha específica",
         tags=["Sorteos"],
         responses={
             200: {
                 "description": "Sorteo encontrado",
                 "content": {
                     "application/json": {
                         "example": {
                             "fecha": "2025-11-29",
                             "dow_es": "Sab",
                             "N1": 20, "N2": 31, "N3": 35, "N4": 36, "N5": 37, "N6": 46,
                             "C": 25, "R": 8, "Joker": "3068183"
                         }
                     }
                 }
             },
             404: {"description": "No hay sorteo en esa fecha"},
             400: {"description": "Formato de fecha inválido"}
         })
def get_sorteo_fecha(fecha: str):
    """Obtiene el sorteo de una fecha específica
    
    - **fecha**: Fecha en formato YYYY-MM-DD (ej: 2025-11-29)
    
    Retorna el sorteo completo si existe, o error 404 si no hay sorteo en esa fecha.
    
    **Ejemplos de fechas válidas:**
    - 2025-11-29 (sorteo más reciente)
    - 2014-01-02 
    - 2013-01-03 (sorteo más antiguo)
    """
    df = load_data()
    try:
        fecha_obj = datetime.strptime(fecha, "%Y-%m-%d")
        sorteo = df[df['fecha'].dt.date == fecha_obj.date()]
        if sorteo.empty:
            raise HTTPException(
                status_code=404, 
                detail=f"No hay sorteo en la fecha {fecha}. Rango disponible: {df['fecha'].min().date()} - {df['fecha'].max().date()}"
            )
        return prepare_response(sorteo)[0]
    except ValueError:
        raise HTTPException(
            status_code=400, 
            detail="Formato de fecha inválido. Use YYYY-MM-DD (ej: 2025-11-29)"
        )

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)