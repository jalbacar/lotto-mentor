FROM python:3.11-slim

WORKDIR /app

# Instalar dependencias
RUN pip install fastapi==0.104.1 uvicorn[standard]==0.24.0 pandas==2.1.3

# Copiar archivos
COPY main.py .
COPY server.py .
COPY data/ ./data/

EXPOSE 8000

# Usar Python para manejar PORT
CMD ["python", "server.py"]