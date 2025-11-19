### Entorno virtual
```
python3 -m venv
```
###  ejecutar entorno virtual
```
source .venv/bin/activate
```
### Instalar fastapi
```
pip install "fastapi[standard]"
```
### Ejecutar Endpoint
```
fastapi dev main.py
```

### Instalar Paquetes dentro de requirements.txt
```
pip install -r requirements.txt
```

### Para actualizar el requirements.txt
```
pip freeze > requirements.txt
```


### Crear base de datos en postgres
```
psql postgres
postgres=# create database devinote;
```

### ver bases de datos
```
postgres=# \l;
```

### Instalar ALembic
```
pip install alembic
```

### Para instalar el driver de postgres en caso de que sea necesario
```
pip install psycopg[binary]
```

### inicializar alembic en el directorio raiz
```
alembic init alembic
```

### Crear la revision
```
alembic revision --autogenerate -m "init schema"
```

### Aplica la última migración pendiente a la base de datos
```
alembic upgrade head
```

### Para revertir un cambio

```
alembic downgrade -1
```

### Build Command
```
pip install -r requirements.txt
```

### Start Command
```
alembic upgrade head && gunicorn-k uvicorn.workers.UvicornWorker -w ${WEB_CONCURRENCY:-2} -b 0.0.0.0:$PORT app.main:app
```