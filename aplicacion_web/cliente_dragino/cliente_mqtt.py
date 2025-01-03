import paho.mqtt.client as mqtt
import logging
import json
import requests
from datetime import datetime

THE_BROKER = "eu1.cloud.thethings.network"
THE_TOPIC = "v3/+/devices/#"
URL_BACKEND = "http://backend:8000"

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def on_connect(client,userdata, flags, rc):
    logger.info(f"Connected to broker with result code {rc}")
    client.subscribe(THE_TOPIC, qos=0)

def on_message(client, userdata, msg):
    logger.info(f"Message received: {msg.topic} -> {msg.payload.decode('utf-8')}")
    print("Se ha recibido un mensaje MQTT del nodo")
    dict_payload = json.loads(msg.payload.decode("utf-8"))
    try:
        decoded_payload = dict_payload.get("uplink_message", {}).get("decoded_payload", {})

        temperature = decoded_payload.get("TempC_SHT31")
        humidity = decoded_payload.get("Hum_SHT31")
        timestamp = decoded_payload.get("Data_time")

        if temperature is not None and humidity is not None and timestamp:
            # Convertir timestamp a datetime
            timestamp = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")

            # Crear el payload para enviar a la API
            sensor_data = {
                "sensor_id": "wimosa-albarracin-trh-drgn",
                "temperature": temperature,
                "humidity": humidity,
                "timestamp": timestamp.isoformat()
            }

            # Enviar los datos al backend API
            response = requests.post(f"{URL_BACKEND}/sensor_data/", json=sensor_data)

            if response.status_code == 200:
                print(f"Data sent successfully: {sensor_data}")
            else:
                print(f"Failed to send data. Status code: {response.status_code}")
        else:
            print("Missing required data (temperature, humidity, or timestamp)")
    except Exception as e:
        print(f"Error sending data: {e}")

if __name__ == "__main__":
    client = mqtt.Client(client_id="",
                         clean_session=True,
                         userdata=None,
                         protocol=mqtt.MQTTv311,
                         transport="tcp")
    
    client.on_connect = on_connect
    client.on_message = on_message

    client.username_pw_set(username="wimosa-albarracin-trh-drgn-app@ttn",
                           password="NNSXS.V4TWHJ4DUC5IIX6IYMDWRZ2552YDDNUZTM7WMAQ.DOWDEAM4AV7MTPASEBAZ73S7SVVJBWHD7CIZG76YYUEKZ6CONCEQ")

    client.connect(THE_BROKER, port=1883, keepalive=60)

    client.loop_forever()
