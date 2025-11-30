import argparse
import logging
from .downloader import LottoDownloader



def main():
    """Función principal CLI"""
    parser = argparse.ArgumentParser(description='Descarga CSV con verificación VPN')
    parser.add_argument('-c', '--config', default='config.ini', help='Archivo de configuración')
    parser.add_argument('-u', '--url', help='URL del CSV (sobrescribe config)')
    parser.add_argument('-o', '--output', help='Ruta de salida (sobrescribe config)')
    
    args = parser.parse_args()
    
    try:
        # Crear downloader con configuración
        downloader = LottoDownloader(args.config)
        
        # Descargar usando argumentos CLI o configuración
        result = downloader.download(args.url, args.output)
        print(f"Descarga completada: {result}")
        
    except Exception as e:
        print(f"Error: {e}")
        logging.error(f"Error en descarga: {e}")

if __name__ == '__main__':
    main()