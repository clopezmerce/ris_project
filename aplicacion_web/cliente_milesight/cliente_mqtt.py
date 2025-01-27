import paho.mqtt.client as mqtt
import logging
import json
import requests
from datetime import datetime

THE_BROKER = "eu1.cloud.thethings.network"
THE_TOPIC = "v3/itaca-mlsght-em320-th-app@ttn/devices/eui-24e124785d441512/up"
URL_BACKEND = "http://backend:8000"

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def on_connect(client,userdata, flags, rc):
    logger.info(f"Connected to broker with result code {rc}")
    client.subscribe(THE_TOPIC)

def on_message(client, userdata, msg):
    logger.info(f"Message received: {msg.topic} -> {msg.payload.decode('utf-8')}")
    print("Se ha recibido un mensaje MQTT")
    dict_payload = json.loads(msg.payload.decode("utf-8"))
    try:
        sensor_id = dict_payload.get("end_device_ids", {}).get("device_id", {})
        decoded_payload = dict_payload.get("uplink_message", {}).get("decoded_payload", {})

        temperature = decoded_payload.get("temperature")
        humidity = decoded_payload.get("humidity")

        if temperature is not None and humidity is not None:
            sensor_data = {
                "sensor_id": sensor_id,
                "temperature": temperature,
                "humidity": humidity,
                "timestamp": datetime.now().isoformat()
            }

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

    client.username_pw_set(username="itaca-mlsght-em320-th-app@ttn",
                           password="NNSXS.6L2V2SVZRRVORN27QWX2NUFT5WHX6F6SSW3YBHY.UCNIYV5ZG357SAVT5AMHEZKDBOEYPUSKUAZT2BNOBTIVYWG5F6CA")

    client.connect(THE_BROKER, port=1883, keepalive=60)

    client.loop_forever()
