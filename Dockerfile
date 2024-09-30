# Usar una imagen base de Python
FROM python:3.9-slim

# Establecer el directorio de trabajo
WORKDIR /app

# Instalar herramientas de construcción
RUN apt-get update && apt-get install -y build-essential

# Copiar y instalar dependencias del backend
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Copiar el código del backend
COPY . /app

# Instalar gunicorn
RUN pip install gunicorn

# Recopilar archivos estáticos de Django
RUN python manage.py collectstatic --noinput

# Exponer el puerto
EXPOSE 8000

# Comando para ejecutar la aplicación
CMD ["gunicorn", "core.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "4"]