#!/usr/bin/env python3
"""
Módulo para transformar el archivo historico_raw.csv a historico_clean.csv
"""

import pandas as pd
import re
from datetime import datetime
import os


class CSVTransformer:
    """Clase para transformar archivos CSV de la Primitiva"""
    
    def __init__(self, input_file, output_file):
        self.input_file = input_file
        self.output_file = output_file
    
    def clean_raw_data(self):
        """
        Limpia el archivo CSV raw eliminando metadatos y procesando solo los datos de sorteos
        """
        try:
            # Leer el archivo completo
            with open(self.input_file, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            # Encontrar la línea de cabecera
            header_line = None
            data_start = None
            
            for i, line in enumerate(lines):
                if 'FECHA' in line and 'N1' in line:
                    header_line = line.strip()
                    data_start = i + 1
                    break
            
            if header_line is None:
                raise ValueError("No se encontró la cabecera del archivo")
            
            # Procesar cabecera
            header = [col.strip() for col in header_line.split(';')]
            
            # Procesar datos
            clean_data = []
            count = 0
            
            for line in lines[data_start:]:
                line = line.strip()
                if not line or line.startswith('***'):
                    continue
                
                # Dividir por punto y coma
                fields = [field.strip() for field in line.split(';')]
                
                if len(fields) >= len(header):
                    # Limpiar campos
                    cleaned_row = []
                    for i, field in enumerate(fields[:len(header)]):
                        # Remover comillas y espacios extra
                        cleaned_field = field.strip().strip("'\"")
                        cleaned_row.append(cleaned_field)
                    
                    clean_data.append(cleaned_row)
                    count += 1
                    
                    # Limitar a 20 líneas como se solicita
                    if count >= 20:
                        break
            
            # Crear DataFrame
            df = pd.DataFrame(clean_data, columns=header)
            
            # Guardar archivo limpio
            df.to_csv(self.output_file, index=False, encoding='utf-8')
            
            print(f"✅ Archivo transformado exitosamente:")
            print(f"   - Archivo origen: {self.input_file}")
            print(f"   - Archivo destino: {self.output_file}")
            print(f"   - Registros procesados: {len(df)}")
            print(f"   - Columnas: {list(df.columns)}")
            
            return df
            
        except Exception as e:
            print(f"❌ Error al procesar el archivo: {str(e)}")
            raise
    
    def get_sample_data(self, num_rows=5):
        """
        Obtiene una muestra de los datos procesados
        """
        try:
            df = pd.read_csv(self.output_file)
            return df.head(num_rows)
        except Exception as e:
            print(f"❌ Error al leer el archivo procesado: {str(e)}")
            return None


def transform_csv(input_path=None, output_path=None):
    """
    Función principal para transformar el CSV
    """
    if input_path is None:
        input_path = "data/historico_raw.csv"
    if output_path is None:
        output_path = "data/historico_clean.csv"
    
    # Verificar que el archivo de entrada existe
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"El archivo {input_path} no existe")
    
    # Crear directorio de salida si no existe
    output_dir = os.path.dirname(output_path)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Crear transformador y procesar
    transformer = CSVTransformer(input_path, output_path)
    df = transformer.clean_raw_data()
    
    return df


if __name__ == "__main__":
    # Rutas por defecto
    input_file = "data/historico_raw.csv"
    output_file = "data/historico_clean.csv"
    
    try:
        df = transform_csv(input_file, output_file)
        
        # Mostrar muestra de datos
        print("\n📊 Muestra de datos procesados:")
        print(df.head().to_string())
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")