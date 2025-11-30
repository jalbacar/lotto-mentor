import logging
import os
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from .config import Config
from .vpn_checker import VPNChecker
from .spiders.csv_spider import CSVSpider

class LottoDownloader:
    """Clase principal para descargar CSV con verificación VPN"""
    
    def __init__(self, config_file='config.ini'):
        self.config = Config(config_file)
        self.vpn_checker = VPNChecker()
        self._setup_logging()
        self.logger = logging.getLogger(__name__)
    
    def _setup_logging(self):
        """Configura logging según configuración"""
        logging.basicConfig(
            level=getattr(logging, self.config.log_level),
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(self.config.log_file, encoding='utf-8'),
                logging.StreamHandler()
            ]
        )
    
    def download(self, url=None, output_path=None):
        """Descarga CSV usando configuración o parámetros"""
        download_url = url or self.config.download_url
        output_file = output_path or self.config.output_path
        
        self.logger.info(f"Iniciando descarga: {download_url} -> {output_file}")
        
        # Verificar VPN si está habilitado
        if self.config.vpn_check_enabled:
            if not self.vpn_checker.is_vpn_active(self.config.vpn_timeout):
                raise ConnectionError("VPN requerida pero no detectada")
        
        # Crear directorio de salida
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        
        # Ejecutar spider
        settings = get_project_settings()
        settings.setmodule('lotto_downloader.settings')
        
        process = CrawlerProcess(settings)
        process.crawl(CSVSpider, 
                      url=download_url, 
                      output_path=output_file,
                      config=self.config)
        process.start()
        
        return output_file
    
    def check_vpn_status(self):
        """Verifica estado de VPN"""
        return self.vpn_checker.is_vpn_active(self.config.vpn_timeout)
    
    def get_config_info(self):
        """Retorna información de configuración"""
        return {
            'url': self.config.download_url,
            'output_path': self.config.output_path,
            'vpn_enabled': self.config.vpn_check_enabled,
            'log_level': self.config.log_level
        }