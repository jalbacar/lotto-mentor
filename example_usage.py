#!/usr/bin/env python3
"""Ejemplo de uso del descargador de CSV"""

from lotto_downloader import LottoDownloader

def download_csv_example():
    """Ejemplo de descarga programática usando POO"""
    
    # Crear instancia del downloader
    downloader = LottoDownloader('config.ini')
    
    # Verificar configuración
    config_info = downloader.get_config_info()
    print(f"Configuración: {config_info}")
    
    # Verificar VPN
    if downloader.check_vpn_status():
        print("VPN activa")
    else:
        print("VPN no detectada")
    
    try:
        # Descargar usando configuración
        result = downloader.download()
        print(f"Descarga exitosa: {result}")
        
        # O descargar con parámetros específicos
        # result = downloader.download(
        #     url="https://otra-url.com/data.csv",
        #     output_path="data/custom.csv"
        # )
        
    except Exception as e:
        print(f"Error en descarga: {e}")

if __name__ == "__main__":
    download_csv_example()