# Usa una imagen base oficial de Python
FROM python:3.11-slim

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /code

# Copia archivos del proyecto
COPY . /code

# Instala dependencias del sistema necesarias
RUN apt-get update && apt-get install -y \
    libpq-dev gcc python3-dev libaio1 && \
    rm -rf /var/lib/apt/lists/*

# Instala dependencias de Python
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Expone el puerto 8000 para acceder desde fuera
EXPOSE 8000

# Comando por defecto
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

