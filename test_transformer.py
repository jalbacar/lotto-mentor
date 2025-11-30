#!/usr/bin/env python3
"""Script de prueba para el transformador."""

from lotto_transformer import LottoTransformer

def main():
    """Ejecuta la transformación de prueba."""
    transformer = LottoTransformer()
    
    input_file = "data/historico_raw.csv"
    output_file = "data/historico_clean_test.csv"
    
    print("🔄 Iniciando transformación...")
    transformer.transform(input_file, output_file)
    print("✅ Transformación completada!")

if __name__ == "__main__":
    main()