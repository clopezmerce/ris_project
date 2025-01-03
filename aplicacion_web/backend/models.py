from pydantic import BaseModel, Field
from datetime import datetime


class SensorData(BaseModel):
    """
    Modelo para representar los datos de un sensor enviados a la API.
    """
    sensor_id: str = Field(..., description="Identificador único del sensor")
    temperature: float = Field(..., description="Valor de la temperatura capturada por el sensor")
    humidity: float = Field(..., description="Valor de la humedad capturada por el sensor", ge=0, le=100)
    timestamp: datetime = Field(..., description="Marca de tiempo en formato ISO 8601")
