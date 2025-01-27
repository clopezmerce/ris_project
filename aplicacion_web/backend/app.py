import asyncio
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dal.influxdb import InfluxDBDAL
from models import SensorData, RakData
from datetime import datetime
import paho.mqtt.client as mqtt
import json
import logging
import os

app = FastAPI()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

TOKEN_FILE = "access_token.txt"

# Función para cargar el token desde un archivo
def load_access_token():
    """Loads the access token from a file if it exists, if not returns an empty string."""
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, "r") as file:
            return file.read().strip()
    logger.info("access_token.txt does not exist. Please access the influxDB panel at localhost:8086, generate a new one and update it through the API at localhost:8000/token/")
    return ""

# Función para guardar el token en un archivo
def save_access_token(token):
    """Guarda el nuevo token en el archivo."""
    with open(TOKEN_FILE, "w") as file:
        file.write(token)
        

#Credentials
ACCESS_TOKEN = load_access_token()
MQTT_BROKER = "eu1.cloud.thethings.network"
MQTT_TOPIC = "v3/upvdisca-rakwireless-rak3172-app@ttn/devices/eui-ac1f09fffe1787e9/down/push"
USERNAME = "upvdisca-rakwireless-rak3172-app@ttn"
PASSWORD = "NNSXS.ZINEMTZWMNGJ2BLIKU7Z33ZDOMX2YR55TH653QI.EGY5E6ZYLNZVUOTXA2W6X3YQFVY5N6ZEEUT3AKNOQB5Q7RVXXAQA"


#Sensor Status
sensor_status = {
    "wimosa albarracin-trh-drgn": True,
    "eui-24e124785d441512": True,
    "eui-ac1f09ffffe1787e9": True,
    "rak_alarm" : False
}

sensor_timers = {}

sensor_timeouts = {
    "wimosa albarracin-trh-drgn": 20 * 60,
    "eui-24e124785d441512": 15 * 60,
    "eui-ac1f09ffffe1787e9": 2 * 60,
}

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

async def sensor_timeout(sensor_id: str):
    """Sets the status of a timed_out sensor to false and loggs the issue."""
    try:
        await asyncio.sleep(sensor_timeouts[sensor_id])
        sensor_status[sensor_id] = False
        logger.warning(f"Sensor {sensor_id} has timed out and is now marked with the False status.")
    except asyncio.CancelledError:
        logger.info(f"{sensor_id}'s timer has been cancelled before expiring.")

def reset_sensor_timer(sensor_id: str):
    """Resets the timer of a sensor to prevent it for falsely timing out."""
    if sensor_id in sensor_timers:
        try:
            sensor_timers[sensor_id].cancel()
        except Exception as e:
            logger.error(f"Problem cancelling the timer of the sensor {sensor_id}: {e}")
    
    sensor_status[sensor_id] = True
    sensor_timers[sensor_id] = asyncio.create_task(sensor_timeout(sensor_id))

@app.on_event("startup")
async def startup_event():
    """Sets a timer for each sensor."""
    for sensor_id in sensor_status.keys():
        sensor_timers[sensor_id] = asyncio.create_task(sensor_timeout(sensor_id))

@app.post("/token/{token}")
async def update_token(token: str):
    """Updates the InfluxDB access token and saves it in a file."""
    global ACCESS_TOKEN, db_dal
    ACCESS_TOKEN = token
    save_access_token(token)
    db_dal = InfluxDBDAL(url="http://influxdb:8086", token=ACCESS_TOKEN, org="carlos_diego", bucket="sensors_bucket")
    logger.info(f"The token {token} has been loaded and saved correctly")
    return {"message": "Token updated successfully!"}   

@app.post("/sensor_data/")
async def save_sensor_data(sensor_data: SensorData):
    """Sends the recieved data to InfluxDB."""
    db_dal.write_data(sensor_data)
    reset_sensor_timer(sensor_data.sensor_id)
    return {"message": "Data saved successfully!"}

@app.post("/rak_data/")
async def save_rak_data(rak_data: RakData):
    """Sends the data recieved from the RAK to InfluxDB."""
    global rak_alarm
    sensor_status["rak_alarm"] = rak_data['alarm']
    sensor_data = SensorData(**rak_data.model_dump(exclude={"alarm"}))
    db_dal.write_data(sensor_data)
    reset_sensor_timer(sensor_data.sensor_id)
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
    """Sends a sensor's requested data."""
    data = db_dal.read_data(sensor_id, start_time, end_time)
    return data

@app.get("/sensors/")
async def get_sensors():
    """Sends a JSON of all the registered sensors."""
    sensors = db_dal.get_unique_sensors()
    return {"sensors": sensors}

@app.get("/sensor_status/")
async def get_sensor_status():
    """Sends a JSON with the status of all the registred sensors."""
    global sensor_status
    return sensor_status
