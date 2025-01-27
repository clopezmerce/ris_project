from influxdb_client import InfluxDBClient
from influxdb_client.client.write_api import Point
from typing import List
from datetime import datetime

class InfluxDBDAL:
    def __init__(self, url: str, token: str, org: str, bucket: str):
        self.client = InfluxDBClient(url=url, token=token, org=org)
        self.bucket = bucket

    def write_data(self, sensor_data):
        write_api = self.client.write_api()
        point = (
            Point("sensor_data")
            .tag("sensor_id", sensor_data.sensor_id)
            .field("temperature", sensor_data.temperature)
            .field("humidity", sensor_data.humidity)
            .time(sensor_data.timestamp)
        )
        write_api.write(self.bucket, record=point)

    def read_data(self, sensor_id: str, start_time: datetime = None, end_time: datetime = None):
        if not start_time:
            start_time = datetime(1970, 1, 1)
    
        if not end_time:
            end_time = datetime.utcnow()

        start_time_str = start_time.strftime('%Y-%m-%dT%H:%M:%SZ')
        end_time_str = end_time.strftime('%Y-%m-%dT%H:%M:%SZ')

        query = f'''
        from(bucket: "{self.bucket}")
            |> range(start: {start_time_str}, stop: {end_time_str})
            |> filter(fn: (r) => r["_measurement"] == "sensor_data" and r["sensor_id"] == "{sensor_id}")
            |> pivot(rowKey:["_time"], columnKey: ["_field"], valueColumn: "_value")
            '''

        query_api = self.client.query_api()
        result = query_api.query(query=query)

        sensor_data_list = []

        for table in result:
            for record in table.records:
                sensor_data_list.append({
                    "sensor_id": record["sensor_id"],
                    "temperature": record["temperature"],
                    "humidity": record["humidity"],
                    "timestamp": record["_time"]
                })

        return sensor_data_list

    def get_unique_sensors(self) -> List[str]:
        query = f'''
        from(bucket: "{self.bucket}")
            |> range(start: -30d)  // Rango de tiempo para obtener los sensores recientes
            |> distinct(column: "sensor_id")
        '''
        query_api = self.client.query_api()
        result = query_api.query(query=query)

        sensors = set()
        for table in result:
            for record in table.records:
                sensor_id = record.values.get("sensor_id")
                if sensor_id:
                    sensors.add(sensor_id)
    
        return list(sensors)
