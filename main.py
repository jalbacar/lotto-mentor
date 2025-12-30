import os
import random
import logging
import pandas as pd
from typing import List, Dict, Any, Optional
from datetime import datetime
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Query, BackgroundTasks
from pydantic import BaseModel, Field

# Configuración de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("lotto_api")

# Constantes
CSV_FILE = "data/historico_clean.csv"
MODEL_DIR = "models"
STAT_FILE = "data/statistical_data.pkl"

# --- Pydantic Models (según openapi.json) ---

class NumberPrediction(BaseModel):
    number: int = Field(..., title="Number", description="Número de lotería (1-49)")
    score: float = Field(..., title="Score", description="Puntuación combinada")
    lstm_score: float = Field(..., title="Lstm Score", description="Puntuación del modelo LSTM")
    stat_score: float = Field(..., title="Stat Score", description="Puntuación estadística")

class PredictionResponse(BaseModel):
    top_numbers: List[NumberPrediction] = Field(..., title="Top Numbers")
    combinations: List[List[int]] = Field(..., title="Combinations")
    metadata: Dict[str, Any] = Field(..., title="Metadata")

class UserPredictionRequest(BaseModel):
    top_n: int = Field(15, title="Top N")
    n_combinations: int = Field(10, title="N Combinations")

# --- Lógica de Negocio / Mock Engine ---

class PredictionEngine:
    def __init__(self):
        self.stats = {}
        self.is_loaded = False

    def load_models(self):
        """
        Carga los modelos LSTM y los datos estadísticos.
        En esta implementación base, calculamos estadísticas desde el CSV si no hay pkl.
        """
        logger.info("Cargando modelos y datos estadísticos...")
        try:
            # Simulación de carga de modelos LSTM
            # self.lstm_models = [load_model(f"lstm_model_{i}.keras") for i in range(1, 6)]
            self.load_statistics()
            self.is_loaded = True
            logger.info("Sistema de predicción listo.")
        except Exception as e:
            logger.error(f"Error cargando modelos: {e}")
            self.is_loaded = False

    def load_statistics(self):
        """Carga o calcula estadísticas básicas del CSV"""
        if os.path.exists(CSV_FILE):
            df = pd.read_csv(CSV_FILE)
            # Calcular frecuencia simple como 'stat_score' base
            numeros = []
            for col in ['N1', 'N2', 'N3', 'N4', 'N5', 'N6']:
                numeros.extend(pd.to_numeric(df[col], errors='coerce').dropna().tolist())
            
            freq_series = pd.Series(numeros).value_counts(normalize=True)
            self.stats = freq_series.to_dict()
        else:
            logger.warning("No se encontró archivo CSV para estadísticas.")
            self.stats = {}

    def predict(self, top_n: int = 15, n_combinations: int = 10) -> PredictionResponse:
        if not self.is_loaded:
            self.load_models()

        # Generar predicciones para todos los números (1-49)
        all_preds = []
        for num in range(1, 50):
            # Obtener estadisticas reales
            stat_score = self.stats.get(float(num), 0.0)
            
            # Simular LSTM score (0 a 1)
            # TODO: Reemplazar con inferencia real de LSTM
            lstm_score = random.random() * 0.5 
            
            # Weighted Fusion (60% LSTM + 40% Stat) según arquitectura
            # Ajustamos escalas para que sean comparables
            # Stat score suele ser bajo (ej 0.02), normalizamos un poco para el ejemplo
            norm_stat = stat_score * 10  # Factor de escala arbitrario para demo
            
            final_score = (0.6 * lstm_score) + (0.4 * norm_stat)
            
            all_preds.append(NumberPrediction(
                number=num,
                score=round(final_score, 4),
                lstm_score=round(lstm_score, 4),
                stat_score=round(stat_score, 6)
            ))
        
        # Ordenar por score descendente
        all_preds.sort(key=lambda x: x.score, reverse=True)
        top_numbers = all_preds[:top_n]
        
        # Generar combinaciones basadas en los top numbers
        # Estrategia simple: Sampling ponderado o aleatorio de los top N
        combinations = []
        top_nums_list = [p.number for p in top_numbers]
        
        if len(top_nums_list) >= 6:
            for _ in range(n_combinations):
                # Elegir 6 números al azar de los top_n
                combo = sorted(random.sample(top_nums_list, min(6, len(top_nums_list))))
                combinations.append(combo)
        
        return PredictionResponse(
            top_numbers=top_numbers,
            combinations=combinations,
            metadata={
                "timestamp": datetime.now().isoformat(),
                "model_version": "1.0.0",
                "total_candidates": len(all_preds)
            }
        )

    def retrain(self):
        """Simula el reentrenamiento o recarga de datos"""
        logger.info("Iniciando proceso de reentrenamiento/recarga...")
        self.load_models()
        return {"status": "success", "message": "Datos recargados y estadísticas actualizadas"}

# Instancia global del motor
engine = PredictionEngine()

# --- FastAPI App ---

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Cargar modelos al inicio
    engine.load_models()
    yield
    # Limpieza al apagar

app = FastAPI(
    title="Lotería Primitiva Prediction API",
    description="AI-powered lottery number predictions using LSTM + Statistics",
    version="1.0.0",
    lifespan=lifespan
)

# --- Endpoints ---

@app.get("/", summary="Root", description="API information endpoint")
def root():
    return {
        "name": "Lotería Primitiva Prediction API",
        "version": "1.0.0",
        "status": "online",
        "docs_url": "/docs"
    }

@app.get("/health", summary="Health Check")
def health_check():
    return {"status": "ok", "engine_loaded": engine.is_loaded}

@app.get("/predict", response_model=PredictionResponse, summary="Predict Lottery")
def predict_lottery(
    top_n: int = Query(15, title="Top N", description="Number of top predictions to return"),
    n_combinations: int = Query(10, title="N Combinations", description="Number of lottery combinations to generate")
):
    """
    Get lottery number predictions.
    
    Parameters:
    - **top_n**: Number of top numbers to return.
    - **n_combinations**: Number of combinations to generate from those numbers.
    """
    return engine.predict(top_n=top_n, n_combinations=n_combinations)

@app.post("/user/predict", response_model=PredictionResponse, summary="User Predict")
def user_predict(request: UserPredictionRequest):
    """
    User-facing prediction endpoint.
    """
    return engine.predict(top_n=request.top_n, n_combinations=request.n_combinations)

@app.post("/admin/retrain", summary="Admin Retrain")
def admin_retrain(background_tasks: BackgroundTasks):
    """
    Trigger data refresh / retraining.
    Reloads statistical data and recomputes scores.
    """
    # Ejecutar en background para no bloquear
    background_tasks.add_task(engine.retrain)
    return {"message": "Retraining started in background"}

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)