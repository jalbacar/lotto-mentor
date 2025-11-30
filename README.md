# Lotto Transformer

Módulo Python para transformar datos históricos de lotería de formato raw a formato clean.

## Instalación

```bash
pip install -e .
```

## Uso

### Como módulo Python

```python
from lotto_transformer import LottoTransformer

transformer = LottoTransformer()
transformer.transform('data/historico_raw.csv', 'data/historico_clean.csv')
```

### Desde línea de comandos

```bash
lotto-transform data/historico_raw.csv data/historico_clean.csv
```

## Transformaciones realizadas

- Convierte fechas del formato `Jue-17-10-1985` a `1985-10-17`
- Extrae el día de la semana en español
- Limpia valores numéricos eliminando espacios
- Mantiene campos vacíos como cadenas vacías
- Genera CSV con encoding UTF-8

## Estructura de datos

### Entrada (raw)
```
FECHA; N1;N2;N3;N4;N5;N6;C;R;Joker;...
Jue-17-10-1985 ; 3;11;13;15;34;35;27;0;;...
```

### Salida (clean)
```
fecha,dow_es,N1,N2,N3,N4,N5,N6,C,R,Joker
1985-10-17,Jue,3,11,13,15,34,35,27,0,
```