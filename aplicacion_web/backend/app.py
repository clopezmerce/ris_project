from fastapi import FastAPI
from dal.influxdb import InfluxDBDAL
from models import SensorData
from datetime import datetime

app = FastAPI()

ACCESS_TOKEN = "cgWnEvJBhPDiish6_vepCia7rjDLBm2mTTK7POEzbySH6yowaMnXVvWyKU1MpYg2Nm5poa2mAISSoSWxRrAUsQ=="

db_dal = InfluxDBDAL(url="http://influxdb:8086", token=ACCESS_TOKEN, org="carlos_diego", bucket="sensors_bucket")


@app.post("/token/{token}")
async def update_token(token: str):
    global db_dal
    ACCESS_TOKEN = token
    db_dal = InfluxDBDAL(url="http://influxdb:8086", token=ACCESS_TOKEN, org="carlos_diego", bucket="sensors_db")
   

@app.post("/sensor_data/")
async def save_sensor_data(sensor_data: SensorData):
    db_dal.write_data(sensor_data)
    return {"message": "Data saved successfully!"}

@app.get("/sensor_data/{sensor_id}/")
async def get_sensor_data(sensor_id: str, start_time: datetime = None, end_time: datetime = None):
    data = db_dal.read_data(sensor_id, start_time, end_time)
    return data

@app.get("/sensors/")
async def get_sensors():
    sensors = db_dal.get_unique_sensors()
    return {"sensors": sensors}
