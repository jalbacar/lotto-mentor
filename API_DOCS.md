# 📚 Lotto Data API - Documentación

## 🌐 Acceso a la API

- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`
- **OpenAPI JSON**: `http://localhost:8000/openapi.json`

## 📋 Endpoints Disponibles

### 🏠 General

#### `GET /`
Información básica de la API y lista de endpoints disponibles.

**Respuesta:**
```json
{
  "message": "Lotto Data API",
  "version": "1.0.0",
  "docs": "/docs",
  "endpoints": [...]
}
```

---

### 🎲 Sorteos

#### `GET /sorteos`
Obtiene sorteos históricos con límite configurable.

**Parámetros:**
- `limit` (opcional): Número máximo de registros (1-1000, default: 100)

**Ejemplo:**
```bash
curl "http://localhost:8000/sorteos?limit=5"
```

**Respuesta:**
```json
[
  {
    "fecha": "2025-11-29",
    "dow_es": "Sab",
    "N1": 20, "N2": 31, "N3": 35, "N4": 36, "N5": 37, "N6": 46,
    "C": 25, "R": 8, "Joker": "3068183"
  }
]
```

#### `GET /sorteos/recientes`
Sorteos de los últimos N días desde la fecha más reciente.

**Parámetros:**
- `dias` (opcional): Días hacia atrás (1-365, default: 30)

**Ejemplo:**
```bash
curl "http://localhost:8000/sorteos/recientes?dias=7"
```

#### `GET /sorteos/fecha/{fecha}`
Obtiene el sorteo de una fecha específica.

**Parámetros:**
- `fecha`: Fecha en formato YYYY-MM-DD

**Ejemplo:**
```bash
curl "http://localhost:8000/sorteos/fecha/2025-11-29"
```

**Errores:**
- `400`: Formato de fecha inválido
- `404`: No hay sorteo en esa fecha

---

### 📊 Estadísticas

#### `GET /estadisticas`
Estadísticas generales del conjunto de datos.

**Respuesta:**
```json
{
  "total_sorteos": 1234,
  "fecha_inicio": "2013-01-03",
  "fecha_fin": "2025-11-29",
  "dias_semana": {
    "Jue": 620,
    "Sab": 614
  }
}
```

#### `GET /numeros/frecuencia`
Frecuencia de aparición de cada número (1-49).

**Respuesta:**
```json
{
  "frecuencia": {
    "1": 45,
    "2": 52,
    "3": 48,
    ...
    "49": 41
  }
}
```

---

## 🔧 Estructura de Datos

### Modelo SorteoResponse
```json
{
  "fecha": "string (YYYY-MM-DD)",
  "dow_es": "string (Lun|Mar|Mie|Jue|Vie|Sab|Dom)",
  "N1": "integer (1-49) | null",
  "N2": "integer (1-49) | null", 
  "N3": "integer (1-49) | null",
  "N4": "integer (1-49) | null",
  "N5": "integer (1-49) | null",
  "N6": "integer (1-49) | null",
  "C": "integer (0-49) | null",
  "R": "integer (0-9) | null",
  "Joker": "string"
}
```

## 📈 Casos de Uso

### 1. Análisis de Frecuencias
```bash
# Obtener números más frecuentes
curl "http://localhost:8000/numeros/frecuencia"
```

### 2. Sorteos Recientes
```bash
# Últimos 10 días
curl "http://localhost:8000/sorteos/recientes?dias=10"
```

### 3. Consulta Histórica
```bash
# Sorteo específico
curl "http://localhost:8000/sorteos/fecha/2014-01-02"
```

### 4. Estadísticas Generales
```bash
# Resumen del dataset
curl "http://localhost:8000/estadisticas"
```

## 🚀 Ejemplos con JavaScript

```javascript
// Obtener sorteos recientes
const response = await fetch('/sorteos/recientes?dias=30');
const sorteos = await response.json();

// Buscar sorteo por fecha
const sorteo = await fetch('/sorteos/fecha/2025-11-29')
  .then(r => r.json());

// Análisis de frecuencias
const freq = await fetch('/numeros/frecuencia')
  .then(r => r.json());
```

## 🐍 Ejemplos con Python

```python
import requests

# Cliente base
base_url = "http://localhost:8000"

# Obtener estadísticas
stats = requests.get(f"{base_url}/estadisticas").json()
print(f"Total sorteos: {stats['total_sorteos']}")

# Sorteos recientes
recientes = requests.get(f"{base_url}/sorteos/recientes?dias=7").json()
print(f"Sorteos última semana: {len(recientes)}")

# Frecuencia de números
freq = requests.get(f"{base_url}/numeros/frecuencia").json()
numeros_top = sorted(freq['frecuencia'].items(), 
                    key=lambda x: x[1], reverse=True)[:10]
print("Top 10 números:", numeros_top)
```

## 🔍 Validaciones

- **Límites**: Los parámetros `limit` y `dias` tienen rangos válidos
- **Fechas**: Formato YYYY-MM-DD obligatorio
- **Errores**: Respuestas HTTP estándar (400, 404, 500)
- **Tipos**: Validación automática con Pydantic

## 📱 Acceso desde Frontend

La API incluye CORS habilitado para desarrollo local. Para producción, configurar dominios específicos.