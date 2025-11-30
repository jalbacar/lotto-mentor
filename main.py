import os
import pandas as pd
from fastapi import FastAPI, HTTPException, Query
from typing import Optional, List, Dict
from datetime import datetime

app = FastAPI(
    title="Lotto Data API",
    description="API para acceder a datos históricos de lotería",
    version="1.0.0"
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
    df['fecha'] = pd.to_datetime(df['fecha'])
    return df.fillna("")

@app.get("/")
def root():
    return {"message": "Lotto Data API - Visita /docs para documentación"}

@app.get("/sorteos")
def get_sorteos(limit: Optional[int] = Query(100, description="Límite de registros")):
    """Obtiene sorteos históricos"""
    df = load_data()
    if limit:
        df = df.head(limit)
    return df.to_dict(orient="records")

@app.get("/sorteos/recientes")
def get_sorteos_recientes(dias: int = Query(30, description="Últimos N días")):
    """Sorteos de los últimos N días"""
    df = load_data()
    fecha_limite = df['fecha'].max() - pd.Timedelta(days=dias)
    df_recientes = df[df['fecha'] >= fecha_limite]
    return df_recientes.to_dict(orient="records")

@app.get("/numeros/frecuencia")
def get_frecuencia_numeros():
    """Frecuencia de aparición de números"""
    df = load_data()
    numeros = []
    for col in ['N1', 'N2', 'N3', 'N4', 'N5', 'N6']:
        numeros.extend(df[col].tolist())
    
    frecuencia = pd.Series(numeros).value_counts().to_dict()
    return {"frecuencia": frecuencia}

@app.get("/estadisticas")
def get_estadisticas():
    """Estadísticas generales"""
    df = load_data()
    return {
        "total_sorteos": len(df),
        "fecha_inicio": df['fecha'].min().isoformat(),
        "fecha_fin": df['fecha'].max().isoformat(),
        "dias_semana": df['dow_es'].value_counts().to_dict()
    }

@app.get("/sorteos/fecha/{fecha}")
def get_sorteo_fecha(fecha: str):
    """Sorteo por fecha específica (YYYY-MM-DD)"""
    df = load_data()
    try:
        fecha_obj = datetime.strptime(fecha, "%Y-%m-%d")
        sorteo = df[df['fecha'].dt.date == fecha_obj.date()]
        if sorteo.empty:
            raise HTTPException(status_code=404, detail="No hay sorteo en esa fecha")
        return sorteo.to_dict(orient="records")[0]
    except ValueError:
        raise HTTPException(status_code=400, detail="Formato de fecha inválido (YYYY-MM-DD)")