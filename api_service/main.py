
from fastapi import FastAPI
import redis
import grpc
import subprocess
from pydantic import BaseModel
import dns_service_pb2
import dns_service_pb2_grpc
import hashlib

app = FastAPI()

# Conexiones a dos instancias de Redis (comentar las que no se usan)
redis_clients = [
    redis.Redis(host='redis1', port=6379, decode_responses=True),
    redis.Redis(host='redis2', port=6379, decode_responses=True),
    redis.Redis(host='redis3', port=6379, decode_responses=True),
    redis.Redis(host='redis4', port=6379, decode_responses=True),
    redis.Redis(host='redis5', port=6379, decode_responses=True),
    redis.Redis(host='redis6', port=6379, decode_responses=True),
    redis.Redis(host='redis7', port=6379, decode_responses=True),
    redis.Redis(host='redis8', port=6379, decode_responses=True),
]

# Variables globales para contar el balance de carga (comentar las que no se usan)
# 2 particiones
#partition_request_count = [0, 0]

# 4 particiones
#partition_request_count = [0, 0, 0, 0]

# 8 particiones
partition_request_count = [0, 0, 0, 0, 0, 0, 0, 0]

class DomainModel(BaseModel):
    domain: str

def get_redis_client(key: str):
    # Selecciona la instancia de Redis basada en el hash (comentar para particionar por)
    index = hash(key) % len(redis_clients)
    
    # Incrementar el contador correspondiente a la partición seleccionada
    partition_request_count[index] += 1
    
    return redis_clients[index]

def get_redis_client_by_range(domain: str):
    # Obtener la primera letra del dominio y convertirla en mayúscula
    first_char = domain[0].upper()
    
    """# Definir las particiones por rango de letras (2 particiones)
    if 'A' <= first_char <= 'M':
        index = 0  # Partición 1: A-M
    else:
        index = 1  # Partición 2: N-Z"""
    
    """# Definir las particiones por rango de letras (4 particiones)
    if 'A' <= first_char <= 'F':
        index = 0  # Partición 1: A-F
    elif 'G' <= first_char <= 'L':
        index = 1  # Partición 2: G-L
    elif 'M' <= first_char <= 'R':
        index = 2  # Partición 3: M-R
    else:
        index = 3  # Partición 4: S-Z"""
    
    # Definir las particiones por rango de letras (8 particiones)
    if 'A' <= first_char <= 'C':
        index = 0  # Partición 1: A-C
    elif 'D' <= first_char <= 'F':
        index = 1  # Partición 2: D-F
    elif 'G' <= first_char <= 'I':
        index = 2  # Partición 3: G-I
    elif 'J' <= first_char <= 'L':
        index = 3  # Partición 4: J-L
    elif 'M' <= first_char <= 'O':
        index = 4  # Partición 5: M-O
    elif 'P' <= first_char <= 'R':
        index = 5  # Partición 6: P-R
    elif 'S' <= first_char <= 'U':
        index = 6  # Partición 7: S-U
    else:
        index = 7  # Partición 8: V-Z

    # Incrementar el contador de la partición correspondiente
    partition_request_count[index] += 1
    
    return redis_clients[index]

@app.get('/resolve/{domain}')
def resolve_domain(domain: str):
    redis_client = get_redis_client(domain)  # Obtener la instancia de Redis por hash (comentar si uso rango)
    #redis_client = get_redis_client_by_range(domain) # Obtener la instancia de Redis por rango (comentar si uso hash)
    
    ip_address = redis_client.get(domain)
    if ip_address:
        return {"domain": domain, "ip_address": ip_address, "cache": "HIT"}
    else:
        with grpc.insecure_channel('dns_service:50051') as channel:
            stub = dns_service_pb2_grpc.DNSResolverStub(channel)
            response = stub.ResolveDomain(dns_service_pb2.DomainRequest(domain=domain))
            ip_address = response.ip_address
            redis_client.set(domain, ip_address)
            return {"domain": domain, "ip_address": ip_address, "cache": "MISS"}

@app.get('/load-balance')
def get_load_balance():
    # Retornar cuántas solicitudes se han enviado a cada partición (comentar las que no se usan)
    return {
        "particion_1": partition_request_count[0],
        "particion_2": partition_request_count[1],
        "particion_3": partition_request_count[2],
        "particion_4": partition_request_count[3],
        "particion_5": partition_request_count[4],
        "particion_6": partition_request_count[5],
        "particion_7": partition_request_count[6],
        "particion_8": partition_request_count[7],
    }




"""
# 1 particion
from fastapi import FastAPI
import redis
import subprocess
import grpc
from pydantic import BaseModel
import dns_service_pb2
import dns_service_pb2_grpc

app = FastAPI()

# Conexion a una instancia de redis
redis_client = redis.Redis(host='redis1', port=6379, decode_responses=True)

class DomainModel(BaseModel):
    domain: str

@app.get('/resolve/{domain}')
def resolve_domain(domain: str):
    # Verificar si el dominio está en caché
    ip_address = redis_client.get(domain)
    if ip_address:
        #print(f"Caché HIT para {domain}")
        return {"domain": domain, "ip_address": ip_address, "cache": "HIT"}
    else:
        #print(f"Caché MISS para {domain}, realizando resolución DNS")
        # Realizar una llamada gRPC al servicio DNS
        with grpc.insecure_channel('dns_service:50051') as channel:
            stub = dns_service_pb2_grpc.DNSResolverStub(channel)
            response = stub.ResolveDomain(dns_service_pb2.DomainRequest(domain=domain))
            ip_address = response.ip_address
            # Almacenar en caché
            redis_client.set(domain, ip_address)
            return {"domain": domain, "ip_address": ip_address, "cache": "MISS"}
"""
