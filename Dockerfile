FROM python:3.11-slim

WORKDIR /app

# Solo dependencias mínimas para API
RUN pip install fastapi==0.104.1 uvicorn[standard]==0.24.0 pandas==2.1.3

# Copiar solo archivos necesarios
COPY main.py .
COPY data/ ./data/

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]