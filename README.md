# tarea1-SD

video: https://youtu.be/lyD7a6ZXfv0
video para tener compasión: https://www.youtube.com/watch?v=b3rNUhDqciM

#### primero comentar en api_service/app.py todo lo que no sea de la cantidad de particiones que vas a usar

#### Inicializa el docker-compose que vayas a utilizar, por ejemplo para 8 particiones:

```bash
docker-compose -f docker-compose.ocho.yml up -d
```

#### Instalar dependencias:

```bash
pip install psycopg2-binary
```

#### Rellenar base de datos:

```bash
/home/codespace/.python/current/bin/python3 /workspaces/tarea1-SD/db_service/populate_db.py
```

#### Generar tráfico:

```bash
/home/codespace/.python/current/bin/python3 /workspaces/tarea1-SD/traffic_generator/traffic_generator.py
```
