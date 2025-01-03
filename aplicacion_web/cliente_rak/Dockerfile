# Usamos una imagen base de Python
FROM python:3.9-slim

# Establecemos el directorio de trabajo en el contenedor
WORKDIR /cliente_rak

# Copiamos los archivos de la aplicación al contenedor
COPY . ./

# Instalamos las dependencias necesarias
RUN pip install --no-cache-dir -r requirements.txt

# Comando para ejecutar el script de cliente MQTT
CMD ["python", "cliente_mqtt.py"]
