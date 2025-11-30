import requests
import logging
import socket

logger = logging.getLogger(__name__)

class VPNChecker:
    """Verifica si hay conexión VPN activa"""
    
    VPN_CHECK_URLS = [
        'https://ipinfo.io/json',
        'https://httpbin.org/ip'
    ]
    
    def __init__(self, expected_vpn_indicators=None):
        self.expected_indicators = expected_vpn_indicators or []
    
    def is_vpn_active(self, timeout=10):
        """Verifica si VPN está activa"""
        try:
            for url in self.VPN_CHECK_URLS:
                try:
                    response = requests.get(url, timeout=timeout)
                    if response.status_code == 200:
                        data = response.json()
                        ip = data.get('ip', data.get('origin', ''))
                        logger.info(f"IP detectada: {ip}")
                        
                        # Verificar si es IP privada o VPN conocida
                        if self._is_vpn_ip(ip):
                            logger.info("Conexión VPN verificada")
                            return True
                        
                except Exception as e:
                    logger.warning(f"Error verificando {url}: {e}")
                    continue
            
            logger.error("No se detectó conexión VPN")
            return False
            
        except Exception as e:
            logger.error(f"Error verificando VPN: {e}")
            return False
    
    def _is_vpn_ip(self, ip):
        """Verifica si la IP indica conexión VPN"""
        # Rangos IP privados comunes de VPN
        private_ranges = [
            '10.', '172.16.', '172.17.', '172.18.', '172.19.',
            '172.20.', '172.21.', '172.22.', '172.23.', '172.24.',
            '172.25.', '172.26.', '172.27.', '172.28.', '172.29.',
            '172.30.', '172.31.', '192.168.'
        ]
        
        # Verificar indicadores personalizados
        if self.expected_indicators:
            return any(indicator in ip for indicator in self.expected_indicators)
        
        # Verificar rangos privados
        return any(ip.startswith(range_ip) for range_ip in private_ranges)