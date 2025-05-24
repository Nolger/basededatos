# Usa Python oficial como base
FROM python:3.11-slim

# Establece el directorio de trabajo
WORKDIR /app

# Instala dependencias del sistema necesarias para PostgreSQL, MySQL y SQL Server
RUN apt-get update && apt-get install -y \
    curl \
    gnupg2 \
    unixodbc \
    unixodbc-dev \
    gcc \
    g++ \
    libssl-dev \
    libpq-dev \
    default-libmysqlclient-dev \
    pkg-config \
    build-essential

# Instala el driver ODBC 18 para SQL Server
RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - && \
    curl https://packages.microsoft.com/config/debian/10/prod.list > /etc/apt/sources.list.d/mssql-release.list && \
    apt-get update && ACCEPT_EULA=Y apt-get install -y msodbcsql18 && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Copia el código fuente
COPY . .

# Instala dependencias Python
RUN pip install --no-cache-dir -r requirements.txt

# Expone el puerto por defecto de Django
EXPOSE 8000

# Comando por defecto al iniciar el contenedor
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

