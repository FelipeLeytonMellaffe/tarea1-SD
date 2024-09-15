import random
import requests
import psycopg2
import time
import statistics
import matplotlib.pyplot as plt
from collections import Counter

API_URL = 'http://localhost:8000/resolve/'

def get_random_domain():
    conn = psycopg2.connect(
        host="localhost", 
        database="domains_db",
        user="user",
        password="password"
    )
    cursor = conn.cursor()

    random_id = random.randint(1, 10000)
    cursor.execute("SELECT domain_name FROM domains WHERE id = %s", (random_id,))
    domain = cursor.fetchone()

    cursor.close()
    conn.close()

    if domain:
        return domain[0]
    else:
        return None

def generate_traffic(num_requests, miss, hit):
    response_times = []
    domain_requests = []  # Lista para almacenar los dominios consultados
    cont = 0
    for _ in range(num_requests):
        cont += 1
        domain = get_random_domain()
        if domain:
            domain_requests.append(domain)  # Registra el dominio consultado
            start_time = time.time()
            response = requests.get(API_URL + domain)
            end_time = time.time()
            response_time = end_time - start_time
            response_times.append(response_time)

            if response.status_code == 200:
                data = response.json()
                print(f"Dominio {cont}: {data['domain']}, IP: {data['ip_address']}, Caché: {data['cache']}, Tiempo de respuesta: {response_time:.4f} segundos")
                if data['cache'] == "MISS":
                    miss += 1
                else:
                    hit += 1
            else:
                print(f"Error al resolver el dominio {domain}")
        else:
            print("No se encontró un dominio")
        time.sleep(0) 

    # Calcular la media y la desviación estándar de los tiempos de respuesta
    avg_response_time = statistics.mean(response_times)
    stddev_response_time = statistics.stdev(response_times) if len(response_times) > 1 else 0.0

    # Mostrar la distribución de frecuencias
    plot_frequency_distribution(domain_requests)

    return miss, hit, avg_response_time, stddev_response_time

def plot_frequency_distribution(domain_requests):
    # Contar cuántas veces se ha consultado cada dominio
    domain_count = Counter(domain_requests)
    
    # Extraer dominios y sus frecuencias
    domains = list(domain_count.keys())
    frequencies = list(domain_count.values())

    # Generar gráfico de barras
    plt.figure(figsize=(10, 6))
    plt.plot(domains, frequencies, linestyle='-', color='blue')
    plt.xlabel('Dominios')
    plt.ylabel('Frecuencia de Consultas')
    plt.title('Distribución de Frecuencias de Consultas a los Dominios')
    plt.xticks(rotation=90)  # Rotar los nombres de los dominios para legibilidad
    plt.tight_layout()  # Ajustar el layout para evitar que los textos se superpongan
    plt.show()

if __name__ == '__main__':
    miss = 0
    hit = 0
    num_requests = 15000  # Número de solicitudes
    miss, hit, avg_response_time, stddev_response_time = generate_traffic(num_requests, miss, hit)
    print(f"Hit: {hit}\nMiss: {miss}")
    print(f"Hit rate: {hit/num_requests*100}%\nMiss rate: {miss/num_requests*100}%")
    print(f"Tiempo de respuesta promedio: {avg_response_time:.4f} segundos")
    print(f"Desviación estándar del tiempo de respuesta: {stddev_response_time:.4f} segundos")
