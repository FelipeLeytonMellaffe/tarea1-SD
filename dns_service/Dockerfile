FROM python:3.9-slim

WORKDIR /app

COPY dns_service.py dns_service_pb2.py dns_service_pb2_grpc.py requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt
RUN apt-get update && apt-get install -y dnsutils

CMD ["python", "dns_service.py"]
