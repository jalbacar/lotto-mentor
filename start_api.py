#!/usr/bin/env python3
"""Script para iniciar la API"""

import uvicorn
import os

def main():
    """Inicia el servidor FastAPI"""
    
    # Verificar que existe el CSV
    if not os.path.exists("data/historico_clean.csv"):
        print("❌ No se encontró data/historico_clean.csv")
        print("🔄 Ejecute primero: python full_pipeline.py")
        return
    
    print("🚀 Iniciando API de Lotería...")
    print("📖 Documentación: http://localhost:8000/docs")
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )

if __name__ == "__main__":
    main()