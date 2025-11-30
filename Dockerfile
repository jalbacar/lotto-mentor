FROM python:3.11-slim

WORKDIR /app

# Solo dependencias mínimas para API
RUN pip install fastapi==0.104.1 uvicorn[standard]==0.24.0 pandas==2.1.3

# Copiar archivos necesarios
COPY main.py .
COPY data/ ./data/
COPY start.sh .

# Hacer ejecutable el script
RUN chmod +x start.sh

EXPOSE 8000

# Usar script de inicio
CMD ["./start.sh"]