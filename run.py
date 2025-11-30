#!/usr/bin/env python3
"""Script principal con opciones"""

import argparse
import sys
from lotto_downloader import LottoDownloader
from lotto_transformer import LottoTransformer

def download_only():
    """Solo descarga"""
    downloader = LottoDownloader('config.ini')
    return downloader.download()

def transform_only(input_file, output_file):
    """Solo transformación"""
    transformer = LottoTransformer()
    transformer.transform(input_file, output_file)
    return output_file

def full_pipeline():
    """Pipeline completo"""
    # Descargar
    raw_file = download_only()
    print(f"✅ Descarga: {raw_file}")
    
    # Transformar
    clean_file = 'data/historico_clean.csv'
    transform_only(raw_file, clean_file)
    print(f"✅ Transformación: {clean_file}")
    
    return clean_file

def main():
    parser = argparse.ArgumentParser(description='Lotto Data Pipeline')
    parser.add_argument('action', choices=['download', 'transform', 'full'],
                       help='Acción a ejecutar')
    parser.add_argument('-i', '--input', help='Archivo de entrada (para transform)')
    parser.add_argument('-o', '--output', help='Archivo de salida (para transform)')
    
    args = parser.parse_args()
    
    try:
        if args.action == 'download':
            result = download_only()
            print(f"Descarga completada: {result}")
            
        elif args.action == 'transform':
            if not args.input or not args.output:
                print("Error: transform requiere -i y -o")
                sys.exit(1)
            result = transform_only(args.input, args.output)
            print(f"Transformación completada: {result}")
            
        elif args.action == 'full':
            result = full_pipeline()
            print(f"Pipeline completo: {result}")
            
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()