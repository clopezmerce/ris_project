# Usar una imagen base de Python
FROM python:3.9-slim

# Establecer el directorio de trabajo dentro del contenedor
WORKDIR /backend

# Copiar el archivo requirements.txt al contenedor
COPY requirements.txt ./

# Instalar las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el resto del código fuente al contenedor
COPY . .

# Exponer el puerto 8000 si usas FastAPI
EXPOSE 8000

# Comando predeterminado para ejecutar la aplicación FastAPI con uvicorn
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
