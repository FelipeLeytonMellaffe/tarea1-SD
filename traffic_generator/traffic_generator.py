import random
import requests
import psycopg2
import time

time.sleep(10)

API_URL = 'http://localhost:8000/resolve/'

def get_random_domain():
    # Conexión a la base de datos PostgreSQL
    conn = psycopg2.connect(
        host="localhost",  # O el nombre del servicio de la base de datos en Docker Compose
        database="domains_db",
        user="user",
        password="password"
    )
    cursor = conn.cursor()

    # Obtener un ID aleatorio entre 1 y 10000
    random_id = random.randint(1, 10000)

    # Consultar el dominio correspondiente al ID aleatorio
    cursor.execute("SELECT domain_name FROM domains WHERE id = %s", (random_id,))
    domain = cursor.fetchone()

    cursor.close()
    conn.close()

    if domain:
        return domain[0]
    else:
        return None

def generate_traffic(num_requests):
    for _ in range(num_requests):
        domain = get_random_domain()
        if domain:
            response = requests.get(API_URL + domain)
            if response.status_code == 200:
                data = response.json()
                print(f"Dominio: {data['domain']}, IP: {data['ip_address']}, Caché: {data['cache']}")
            else:
                print(f"Error al resolver el dominio {domain}")
        else:
            print("No se encontró un dominio")
        time.sleep(10)  # Tiempo de espera entre solicitudes

if __name__ == '__main__':
    num_requests = 30000
    generate_traffic(num_requests)
