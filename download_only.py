#!/usr/bin/env python3
"""Script para solo descargar CSV"""

from lotto_downloader import LottoDownloader

def main():
    """Ejecuta solo la descarga"""
    try:
        downloader = LottoDownloader('config.ini')
        result = downloader.download()
        print(f"✅ Descarga completada: {result}")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()