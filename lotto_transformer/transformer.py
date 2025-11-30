import pandas as pd
from datetime import datetime
from typing import Optional

class LottoTransformer:
    """Transformador de datos históricos de lotería."""
    
    def __init__(self):
        self.dow_mapping = {
            'Monday': 'Lun', 'Tuesday': 'Mar', 'Wednesday': 'Mie', 
            'Thursday': 'Jue', 'Friday': 'Vie', 'Saturday': 'Sab', 'Sunday': 'Dom'
        }
    
    def parse_date(self, date_str: str) -> tuple:
        """Convierte fecha DD/MM/YYYY a YYYY-MM-DD y extrae día de semana."""
        date_str = str(date_str).strip()
        try:
            # Parsear DD/MM/YYYY
            date_obj = datetime.strptime(date_str, '%d/%m/%Y')
            formatted_date = date_obj.strftime('%Y-%m-%d')
            
            # Obtener día de semana en español
            dow_en = date_obj.strftime('%A')
            dow_es = self.dow_mapping.get(dow_en, 'Jue')  # Default Jue
            
            return formatted_date, dow_es
        except ValueError:
            return date_str, 'Jue'
    
    def clean_numeric_value(self, value) -> Optional[int]:
        """Limpia valores numéricos."""
        if pd.isna(value) or value == '':
            return None
        try:
            return int(str(value).strip())
        except (ValueError, TypeError):
            return None
    
    def transform(self, input_file: str, output_file: str) -> None:
        """Transforma archivo raw a formato clean."""
        # Leer CSV con formato actual
        df = pd.read_csv(input_file, encoding='utf-8')
        
        clean_data = []
        
        for _, row in df.iterrows():
            # Parsear fecha
            fecha_clean, dow = self.parse_date(row['FECHA'])
            
            # Extraer números de combinación (columnas 1-6)
            numeros = []
            for i in range(1, 7):
                col_name = df.columns[i]  # Columnas de números
                numeros.append(self.clean_numeric_value(row[col_name]))
            
            # Complementario y Reintegro
            comp = self.clean_numeric_value(row['COMP.'])
            reintegro = self.clean_numeric_value(row['R.'])
            
            # Joker
            joker = str(row.get('JOKER', '')).strip()
            if joker == 'nan' or pd.isna(joker):
                joker = ''
            
            clean_row = {
                'fecha': fecha_clean,
                'dow_es': dow,
                'N1': numeros[0],
                'N2': numeros[1], 
                'N3': numeros[2],
                'N4': numeros[3],
                'N5': numeros[4],
                'N6': numeros[5],
                'C': comp,
                'R': reintegro,
                'Joker': joker
            }
            
            clean_data.append(clean_row)
        
        # Guardar CSV limpio
        clean_df = pd.DataFrame(clean_data)
        clean_df.to_csv(output_file, index=False, encoding='utf-8')
        
        print(f"✅ Transformación completada: {len(clean_data)} registros")
        print(f"📁 Guardado en: {output_file}")