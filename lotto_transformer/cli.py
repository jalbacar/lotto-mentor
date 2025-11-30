#!/usr/bin/env python3
"""CLI para el transformador de datos de lotería."""

import argparse
import sys
from pathlib import Path
from .transformer import LottoTransformer


def main():
    """Función principal del CLI."""
    parser = argparse.ArgumentParser(
        description="Transforma datos históricos de lotería de raw a clean"
    )
    
    parser.add_argument(
        "input_file",
        help="Archivo CSV de entrada (formato raw)"
    )
    
    parser.add_argument(
        "output_file", 
        help="Archivo CSV de salida (formato clean)"
    )
    
    args = parser.parse_args()
    
    # Verificar que el archivo de entrada existe
    input_path = Path(args.input_file)
    if not input_path.exists():
        print(f"❌ Error: El archivo {args.input_file} no existe")
        sys.exit(1)
    
    # Crear directorio de salida si no existe
    output_path = Path(args.output_file)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Ejecutar transformación
    try:
        transformer = LottoTransformer()
        transformer.transform(args.input_file, args.output_file)
    except Exception as e:
        print(f"❌ Error durante la transformación: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()