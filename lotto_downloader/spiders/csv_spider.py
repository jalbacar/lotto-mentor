import scrapy
import logging
import os
from urllib.parse import urlparse
from ..vpn_checker import VPNChecker

logger = logging.getLogger(__name__)

class CSVSpider(scrapy.Spider):
    name = 'csv_downloader'
    
    def __init__(self, url=None, output_path=None, config=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.config = config
        self.start_urls = [url] if url else []
        self.output_path = output_path or 'downloaded.csv'
        self.vpn_checker = VPNChecker()
    
    def start_requests(self):
        """Inicia requests solo si VPN está activa"""
        logger.info("Iniciando descarga de CSV")
        
        # Verificar VPN si está habilitado
        if self.config and self.config.vpn_check_enabled:
            timeout = self.config.vpn_timeout if self.config else 10
            if not self.vpn_checker.is_vpn_active(timeout):
                logger.error("VPN no detectada. Abortando descarga.")
                print("ERROR: Conexión VPN requerida. Verifique su VPN y reintente.")
                return
        else:
            logger.info("Verificación VPN deshabilitada")
        
        logger.info("VPN verificada. Iniciando descarga...")
        
        for url in self.start_urls:
            logger.info(f"Solicitando: {url}")
            yield scrapy.Request(
                url=url,
                callback=self.parse_csv,
                errback=self.handle_error
            )
    
    def parse_csv(self, response):
        """Procesa la respuesta CSV"""
        logger.info(f"Respuesta recibida: {response.status} - {len(response.body)} bytes")
        
        if response.status == 200:
            try:
                # Guardar CSV
                os.makedirs(os.path.dirname(self.output_path), exist_ok=True)
                with open(self.output_path, 'wb') as f:
                    f.write(response.body)
                
                logger.info(f"CSV guardado exitosamente en: {self.output_path}")
                print(f"Descarga completada: {self.output_path}")
                
            except Exception as e:
                logger.error(f"Error guardando archivo: {e}")
                print(f"Error guardando archivo: {e}")
        else:
            logger.error(f"Error HTTP: {response.status}")
            print(f"Error descargando: HTTP {response.status}")
    
    def handle_error(self, failure):
        """Maneja errores de conexión"""
        logger.error(f"Error de conexión: {failure.value}")
        print(f"Error de conexión: {failure.value}")