from fastapi import FastAPI
import redis
import subprocess
import grpc
from pydantic import BaseModel
import dns_service_pb2
import dns_service_pb2_grpc

app = FastAPI()
redis_client = redis.Redis(host='redis1', port=6379, decode_responses=True)  # Asegúrate de que 'redis1' coincide con el nombre del servicio en docker-compose

class DomainModel(BaseModel):
    domain: str

@app.get('/resolve/{domain}')
def resolve_domain(domain: str):
    # Verificar si el dominio está en caché
    ip_address = redis_client.get(domain)
    if ip_address:
        return {"domain": domain, "ip_address": ip_address, "cache": "HIT"}
    else:
        # Realizar una llamada gRPC al servicio DNS
        with grpc.insecure_channel('dns_service:50051') as channel:
            stub = dns_service_pb2_grpc.DNSResolverStub(channel)
            response = stub.ResolveDomain(dns_service_pb2.DomainRequest(domain=domain))
            ip_address = response.ip_address
            # Almacenar en caché
            redis_client.set(domain, ip_address)
            return {"domain": domain, "ip_address": ip_address, "cache": "MISS"}
