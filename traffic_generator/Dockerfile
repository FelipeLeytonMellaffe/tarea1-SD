FROM python:3.9-slim

WORKDIR /app

# Copia el script y los archivos necesarios
COPY wait-for-it.sh ./
COPY . .

RUN pip install -r requirements.txt

#CMD ["./wait-for-it.sh", "postgres:5432", "--", "python", "traffic_generator.py"]
