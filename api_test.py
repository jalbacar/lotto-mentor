#!/usr/bin/env python3
"""Script para probar la API de lotería"""

import requests
import json
from datetime import datetime, timedelta

BASE_URL = "http://localhost:8000"

def test_api():
    """Prueba todos los endpoints de la API"""
    
    # Usar fechas reales del CSV actual (2013-2025)
    endpoints = [
        "/",
        "/sorteos?limit=3",
        "/sorteos/recientes?dias=30", 
        "/numeros/frecuencia",
        "/estadisticas",
        "/sorteos/fecha/2025-11-29",  # Fecha real del CSV
        "/sorteos/fecha/2014-01-02"   # Otra fecha real
    ]
    
    print("🧪 Probando API de Lotería...")
    
    for endpoint in endpoints:
        try:
            response = requests.get(f"{BASE_URL}{endpoint}")
            print(f"\n✅ {endpoint}")
            print(f"Status: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                if isinstance(data, list):
                    print(f"Registros: {len(data)}")
                    if data and len(data) > 0:
                        print(f"Primer registro: {data[0]}")
                elif isinstance(data, dict):
                    print(f"Claves: {list(data.keys())}")
                    # Mostrar algunos valores para verificar
                    if 'frecuencia' in data:
                        freq = data['frecuencia']
                        top_nums = sorted(freq.items(), key=lambda x: x[1], reverse=True)[:5]
                        print(f"Top 5 números: {top_nums}")
                    elif 'total_sorteos' in data:
                        print(f"Total sorteos: {data['total_sorteos']}")
                        print(f"Rango fechas: {data.get('fecha_inicio')} - {data.get('fecha_fin')}")
            else:
                print(f"Error: {response.text}")
                
        except requests.exceptions.ConnectionError:
            print(f"❌ {endpoint}: API no disponible. ¿Está ejecutándose el servidor?")
        except Exception as e:
            print(f"❌ {endpoint}: {e}")
    
    print("\n📊 Resumen de pruebas completado")

def test_specific_features():
    """Pruebas específicas de funcionalidades"""
    print("\n🔍 Pruebas específicas...")
    
    # Test de límites
    try:
        response = requests.get(f"{BASE_URL}/sorteos?limit=1")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Límite funciona: {len(data)} registro(s)")
    except:
        print("❌ Error en test de límite")
    
    # Test de fecha inválida
    try:
        response = requests.get(f"{BASE_URL}/sorteos/fecha/2000-01-01")
        if response.status_code == 404:
            print("✅ Manejo correcto de fecha inexistente")
        else:
            print(f"⚠️ Fecha inexistente retornó: {response.status_code}")
    except:
        print("❌ Error en test de fecha inválida")

if __name__ == "__main__":
    test_api()
    test_specific_features()