import grpc
from concurrent import futures
import dns_service_pb2
import dns_service_pb2_grpc
import subprocess

class DNSResolver(dns_service_pb2_grpc.DNSResolverServicer):
    def ResolveDomain(self, request, context):
        domain = request.domain
        # Ejecutar el comando DIG para obtener la dirección IP sin utilizar caché
        result = subprocess.run(['dig', '+noall', '+answer', '+nocmd', '+noauth', '+noadditional', '+nostats', domain], stdout=subprocess.PIPE, text=True)
        output = result.stdout.strip()
        if output:
            # Parsear la salida para obtener la IP
            ip_address = output.split()[-1]
        else:
            ip_address = 'null'
        return dns_service_pb2.DomainResponse(ip_address=ip_address)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    dns_service_pb2_grpc.add_DNSResolverServicer_to_server(DNSResolver(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
