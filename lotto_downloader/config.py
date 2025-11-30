import configparser
import os
import logging

logger = logging.getLogger(__name__)

class Config:
    """Maneja configuración desde archivo INI"""
    
    def __init__(self, config_file='config.ini'):
        self.config = configparser.ConfigParser()
        self.config_file = config_file
        self.load_config()
    
    def load_config(self):
        """Carga configuración desde archivo INI"""
        if os.path.exists(self.config_file):
            self.config.read(self.config_file, encoding='utf-8')
            logger.info(f"Configuración cargada desde: {self.config_file}")
        else:
            logger.warning(f"Archivo de configuración no encontrado: {self.config_file}")
            self._create_default_config()
    
    def _create_default_config(self):
        """Crea configuración por defecto"""
        self.config['download'] = {
            'url': 'https://example.com/data.csv',
            'output_path': 'data/downloaded.csv'
        }
        self.config['vpn'] = {
            'check_enabled': 'true',
            'timeout': '10'
        }
        self.config['logging'] = {
            'level': 'INFO',
            'file': 'lotto_downloader.log'
        }
    
    @property
    def download_url(self):
        return self.config.get('download', 'url')
    
    @property
    def output_path(self):
        return self.config.get('download', 'output_path')
    
    @property
    def vpn_check_enabled(self):
        return self.config.getboolean('vpn', 'check_enabled', fallback=True)
    
    @property
    def vpn_timeout(self):
        return self.config.getint('vpn', 'timeout', fallback=10)
    
    @property
    def log_level(self):
        return self.config.get('logging', 'level', fallback='INFO')
    
    @property
    def log_file(self):
        return self.config.get('logging', 'file', fallback='lotto_downloader.log')
    
    @property
    def delay_min(self):
        return self.config.getint('anti_ban', 'delay_min', fallback=2)
    
    @property
    def delay_max(self):
        return self.config.getint('anti_ban', 'delay_max', fallback=5)
    
    @property
    def retry_times(self):
        return self.config.getint('anti_ban', 'retry_times', fallback=3)
    
    @property
    def concurrent_requests(self):
        return self.config.getint('anti_ban', 'concurrent_requests', fallback=1)