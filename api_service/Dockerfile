FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9-slim

WORKDIR /app

COPY main.py dns_service_pb2.py dns_service_pb2_grpc.py requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt
RUN apt-get update && apt-get install -y curl

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
