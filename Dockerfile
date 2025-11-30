FROM python:3.11-slim

WORKDIR /app

RUN pip install fastapi==0.104.1 uvicorn[standard]==0.24.0 pandas==2.1.3

COPY main.py .
COPY data/ ./data/

EXPOSE 8000

CMD ["python", "main.py"]