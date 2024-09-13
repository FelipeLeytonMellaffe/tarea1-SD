FROM postgres:latest

ENV POSTGRES_DB=domains_db
ENV POSTGRES_USER=user
ENV POSTGRES_PASSWORD=password

# Copiar el script de inicialización SQL y el archivo CSV a la carpeta de inicialización
COPY init.sql /docker-entrypoint-initdb.d/
COPY data/dominios_reducido.csv /docker-entrypoint-initdb.d/

# Copiar el script para poblar la base de datos
COPY populate_db.py /docker-entrypoint-initdb.d/

