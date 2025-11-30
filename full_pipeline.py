#!/usr/bin/env python3
"""Pipeline completo: descarga + transformación"""

from lotto_downloader import LottoDownloader
from lotto_transformer import LottoTransformer
import os

def main():
    """Ejecuta descarga y transformación completa"""
    try:
        # 1. Descargar CSV
        print("🔄 Iniciando descarga...")
        downloader = LottoDownloader('config.ini')
        raw_file = downloader.download()
        print(f"✅ Descarga completada: {raw_file}")
        
        # 2. Transformar datos
        print("🔄 Iniciando transformación...")
        transformer = LottoTransformer()
        clean_file = 'data/historico_clean.csv'
        transformer.transform(raw_file, clean_file)
        print(f"✅ Transformación completada: {clean_file}")
        
        # 3. Mostrar estadísticas
        if os.path.exists(clean_file):
            with open(clean_file, 'r', encoding='utf-8') as f:
                lines = len(f.readlines()) - 1  # -1 por header
            print(f"📊 Registros procesados: {lines}")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()