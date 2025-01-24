from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dal.influxdb import InfluxDBDAL
from models import SensorData
from datetime import datetime
import paho.mqtt.client as mqtt
import json
import logging

app = FastAPI()

ACCESS_TOKEN = "cgWnEvJBhPDiish6_vepCia7rjDLBm2mTTK7POEzbySH6yowaMnXVvWyKU1MpYg2Nm5poa2mAISSoSWxRrAUsQ=="
MQTT_BROKER = "eu1.cloud.thethings.network"
MQTT_TOPIC = "v3/upvdisca-rakwireless-rak3172-app@ttn/devices/eui-ac1f09fffe1787e9/down/push"
USERNAME = "upvdisca-rakwireless-rak3172-app@ttn"
PASSWORD = "NNSXS.ZINEMTZWMNGJ2BLIKU7Z33ZDOMX2YR55TH653QI.EGY5E6ZYLNZVUOTXA2W6X3YQFVY5N6ZEEUT3AKNOQB5Q7RVXXAQA"

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

db_dal = InfluxDBDAL(url="http://influxdb:8086", token=ACCESS_TOKEN, org="carlos_diego", bucket="sensors_bucket")

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        logger.info("Connected to TTN MQTT broker successfully")
    else:
        logger.error(f"Failed to connect, return code {rc}")


mqtt_client = mqtt.Client()
mqtt_client.on_connect = on_connect
mqtt_client.username_pw_set(USERNAME, PASSWORD)
mqtt_client.connect(MQTT_BROKER, port=1883, keepalive=60)
mqtt_client.loop_start()

# CORS Configuration
origins = [
    "http://localhost:3000",  # Frontend URL
]

# Add CORS middleware to the app
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Allow requests from localhost:3000
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headerss
)

@app.post("/token/{token}")
async def update_token(token: str):
    global db_dal
    ACCESS_TOKEN = token
    db_dal = InfluxDBDAL(url="http://influxdb:8086", token=ACCESS_TOKEN, org="carlos_diego", bucket="sensors_db")
   

@app.post("/sensor_data/")
async def save_sensor_data(sensor_data: SensorData):
    db_dal.write_data(sensor_data)
    return {"message": "Data saved successfully!"}

@app.post("/turn_off_led/")
async def turn_off_light():
    """Send command to turn off the LED"""
    try:
        command = {
            "downlinks" : [
                {
                    "f_port": 1,
                    "frm_payload": "AQ==",
                    "confirmed": False
                }
            ]
        }

        payload_str = json.dumps(command)
        mqtt_client.publish(MQTT_TOPIC, payload_str, qos=1)
        
        logger.info(f"Sent command to turn off light: {payload_str}")
        return {"message": "Turn off command sent"}
    except Exception as e:
        logger.error(f"Error sending command: {e}")
        return {"error": str(e)}

@app.get("/sensor_data/{sensor_id}/")
async def get_sensor_data(sensor_id: str, start_time: datetime = None, end_time: datetime = None):
    data = db_dal.read_data(sensor_id, start_time, end_time)
    return data

@app.get("/sensors/")
async def get_sensors():
    sensors = db_dal.get_unique_sensors()
    return {"sensors": sensors}
