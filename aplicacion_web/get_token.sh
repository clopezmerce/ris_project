# get_token.sh
# Usar curl para hacer una consulta a la API de InfluxDB
INFLUXDB_URL="http://influxdb:8086"
INFLUXDB_USERNAME="admin"
INFLUXDB_PASSWORD="adminpassword"
INFLUXDB_ORG="carlos_diego"

# Autenticación de InfluxDB para obtener el token (esto es un ejemplo, puede variar dependiendo de tu configuración)
TOKEN=$(curl -s -X POST "$INFLUXDB_URL/api/v2/authorizations" \
  -H "Content-Type: application/json" \
  -u "$INFLUXDB_USERNAME:$INFLUXDB_PASSWORD" \
  -d '{
        "org": "'$INFLUXDB_ORG'",
        "permissions": [
          {
            "action": "read",
            "resource": { "type": "buckets" }
          }
        ]
      }' | jq -r '.token')

# Crear un archivo temporal o enviar el token al contenedor del backend
echo $TOKEN > /tmp/influxdb_token.txt
