# ris_project

Trabajo para la asignatura Redes Inalámbricas de Sensores MUICC

## Instructions

In order to launch the web application docker and docker-compose are needed.

Once the docker-related services have been started we must execute:


```bash
cd aplicacion_web
docker-compose up --build # or just docker-compose up if it's not the first time
```

**On first startup**


With the web application running we need to create an InfluxDB access token. To do this we can:

1. Connect to the InfluxDB administration pannel in localhost:8086.
2. Authenticate with username: admin and password: adminpassword.
3. Go to the API TOKENS submenu in the LOAD DATA section.
4. Create a new API TOKEN and copy it.
5. Upload the new API TOKEN to the web application through the API using the POST method on localhost:8000/token/*new_access_token*

**With an uploaded access token**
Connect to the frontend at localhost:3000
