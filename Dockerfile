# Usar una imagen base de Python
FROM python:3.9-slim-bullseye

# Configura variables de entorno
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_DEFAULT_TIMEOUT=120 \
    LC_ALL=C.UTF-8 \
    LANG=C.UTF-8

# Instala herramientas necesarias para construir paquetes de Python y Node.js
RUN apt-get update \
    && apt-get install --yes --no-install-recommends \
    gcc \
    g++ \
    build-essential \
    software-properties-common \
    git \
    python3-dev \
    curl

# Establecer el directorio de trabajo
WORKDIR /app

# Instalar herramientas de construcción
RUN apt-get update && apt-get install -y build-essential

# Copiar y instalar dependencias del backend
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Copiar el código del backend
COPY . .

# Recopilar archivos estáticos de Django
RUN python manage.py collectstatic --noinput

# Exponer el puerto
EXPOSE 8000

# Comando para ejecutar la aplicación
CMD ["uwsgi", "--http", ":8000", "--wsgi-file", "app.py", "--callable", "app", "--master", "--processes", "4", "--threads", "2", "--http-timeout", "3000"]