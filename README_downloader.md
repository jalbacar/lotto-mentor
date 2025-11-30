# Lotto CSV Downloader

Módulo Python con Scrapy para descargar archivos CSV con verificación obligatoria de conexión VPN.

## Características

- ✅ Verificación automática de conexión VPN antes de descargar
- 📝 Logging completo de todas las operaciones
- 🕷️ Basado en Scrapy para descargas robustas
- 🛡️ Headers de navegador para evitar bloqueos
- 📁 Creación automática de directorios de salida

## Instalación

```bash
pip install -r requirements_downloader.txt
pip install -e . -f setup_downloader.py
```

## Uso

### Línea de comandos

```bash
# Descargar CSV con verificación VPN
lotto-download https://example.com/data.csv -o data/mi_archivo.csv
```

### Como módulo Python

```python
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from lotto_downloader.spiders.csv_spider import CSVSpider

# Configurar
settings = get_project_settings()
settings.setmodule('lotto_downloader.settings')

# Descargar
process = CrawlerProcess(settings)
process.crawl(CSVSpider, 
              url="https://example.com/data.csv", 
              output_path="data/archivo.csv")
process.start()
```

## Verificación VPN

El módulo verifica automáticamente:
- IP pública actual
- Rangos de IP privados comunes de VPN
- Indicadores personalizados configurables

Si no detecta VPN:
- ❌ Aborta la descarga
- 📝 Registra error en log
- 💬 Muestra mensaje en consola

## Logging

Todas las operaciones se registran en:
- **Consola**: Mensajes importantes
- **Archivo**: `lotto_downloader.log` (completo)

Eventos registrados:
- Verificación de VPN
- Inicio de descarga
- Respuestas HTTP
- Errores de conexión
- Guardado de archivos

## Configuración

Editar `lotto_downloader/settings.py` para:
- Cambiar User-Agent
- Ajustar timeouts
- Modificar delays entre requests
- Configurar headers adicionales