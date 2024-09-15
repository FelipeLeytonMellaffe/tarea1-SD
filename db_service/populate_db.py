import csv
import psycopg2
import time

# Esperar a que la base de datos esté lista
time.sleep(10)

# Conectar a la base de datos PostgreSQL
conn = psycopg2.connect(
    host="localhost",  # El nombre del servicio de la base de datos en Docker Compose
    database="domains_db",
    user="user",
    password="password"
)

cursor = conn.cursor()

# Leer el archivo CSV y poblar la base de datos
with open('data/dominios_reducido.csv', 'r') as f:
    reader = csv.reader(f)
    for row in reader:
        domain = row[0]
        cursor.execute("INSERT INTO domains (domain_name) VALUES (%s)", (domain,))
    conn.commit()

cursor.close()
conn.close()

print("Base de datos poblada con dominios.")
