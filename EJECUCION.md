# Guía de Ejecución - Lotto Data Pipeline

## 📋 Instalación

```bash
# Instalar dependencias
pip install -r requirements_downloader.txt
pip install -e . -f setup_downloader.py
pip install -e .
pip install fastapi uvicorn pandas
```

## 🚀 Modos de Ejecución

### 1. Solo Descarga CSV

```bash
# Opción recomendada
python download_only.py

# Alternativas
lotto-download
python run.py download
```

**Resultado**: Descarga `data/historico_raw.csv`

### 2. Pipeline Completo (Descarga + Transformación)

```bash
# Opción recomendada
python full_pipeline.py

# Alternativa
python run.py full
```

**Resultado**: Genera `data/historico_clean.csv` listo para API

### 3. Solo Transformación

```bash
# CLI transformer
lotto-transform data/historico_raw.csv data/historico_clean.csv

# Script principal
python run.py transform -i data/historico_raw.csv -o data/historico_clean.csv
```

### 4. API FastAPI (Servir Datos)

```bash
# Iniciar servidor API
python start_api.py

# Alternativa manual
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

**Acceso**: 
- API: http://localhost:8000
- Documentación: http://localhost:8000/docs

### 5. Probar API

```bash
# Ejecutar tests automáticos
python api_test.py

# Pruebas manuales
curl http://localhost:8000/sorteos?limit=5
curl http://localhost:8000/estadisticas
```

---

## 🌐 Endpoints API

| Endpoint | Descripción |
|----------|-------------|
| `GET /` | Información básica |
| `GET /sorteos` | Sorteos históricos |
| `GET /sorteos/recientes?dias=30` | Últimos N días |
| `GET /numeros/frecuencia` | Frecuencia números |
| `GET /estadisticas` | Estadísticas generales |
| `GET /sorteos/fecha/1985-10-17` | Sorteo específico |

## ⚙️ Configuración

```ini
[download]
url = https://docs.google.com/spreadsheets/d/.../output=csv
output_path = data/historico_raw.csv

[vpn]
check_enabled = false

[anti_ban]
delay_min = 2
delay_max = 5
```

## 📊 Flujo Completo Recomendado

```bash
# 1. Ejecutar pipeline completo
python full_pipeline.py

# 2. Iniciar API
python start_api.py

# 3. Probar endpoints
python api_test.py
```

## 🔧 Solución de Problemas

### API no inicia:
```bash
# Verificar que existe el CSV limpio
ls data/historico_clean.csv

# Si no existe, ejecutar pipeline
python full_pipeline.py
```

### Error de conexión descarga:
- Verificar URL en `config.ini`
- Revisar logs en `lotto_downloader.log`
- Deshabilitar VPN si es necesario

## 📁 Estructura Final

```
LottoAppTest/
├── config.ini              # Configuración
├── full_pipeline.py        # Pipeline completo
├── start_api.py           # Iniciar API
├── api_test.py            # Probar API
├── main.py                # FastAPI app
├── data/
│   ├── historico_raw.csv   # Datos descargados
│   └── historico_clean.csv # Datos para API
└── logs/                  # Archivos de log
```