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
        # Si no se pasa un start_time, usamos el 1 de enero de 1970 como inicio
        if not start_time:
            start_time = datetime(1970, 1, 1)
    
        # Si no se pasa un end_time, usamos la fecha y hora actual
        if not end_time:
            end_time = datetime.utcnow()

        # Asegúrate de convertir las fechas a formato ISO 8601 sin "Z" para la consulta de InfluxDB
        start_time_str = start_time.strftime('%Y-%m-%dT%H:%M:%SZ')  # Formato sin "Z"
        end_time_str = end_time.strftime('%Y-%m-%dT%H:%M:%SZ')      # Formato sin "Z"

        # Consulta con la fecha correctamente formateada para Flux
        query = f'''
        from(bucket: "{self.bucket}")
            |> range(start: {start_time_str}, stop: {end_time_str})
            |> filter(fn: (r) => r["_measurement"] == "sensor_data" and r["sensor_id"] == "{sensor_id}")
            |> pivot(rowKey:["_time"], columnKey: ["_field"], valueColumn: "_value")
            '''

        query_api = self.client.query_api()
        result = query_api.query(query=query)

        # Procesar y devolver los datos
        sensor_data_list = []

        for table in result:
            for record in table.records:
                # Acceder directamente a las etiquetas y campos
                sensor_data_list.append({
                    "sensor_id": record["sensor_id"],  # Usar directamente "sensor_id" como etiqueta
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

        # Usar un conjunto para asegurarse de que los valores sean únicos
        sensors = set()
        for table in result:
            for record in table.records:
                # Acceder a la etiqueta 'sensor_id'
                sensor_id = record.values.get("sensor_id")
                if sensor_id:
                    sensors.add(sensor_id)  # Agregar al conjunto
    
        return list(sensors)  # Convertir de nuevo a lista para devolverla
