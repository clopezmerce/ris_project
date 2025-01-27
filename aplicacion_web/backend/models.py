from pydantic import BaseModel, Field
from datetime import datetime


class SensorData(BaseModel):
    """
    Model for the sensor data sent throught the API
    """
    sensor_id: str = Field(..., description="Node Identifier")
    temperature: float = Field(..., description="Temperature value captured by the sensor")
    humidity: float = Field(..., description="Relative humidity value captured by the sensor", ge=0, le=100)
    timestamp: datetime = Field(..., description="Timestamp in ISO 8601 format")

class RakData(SensorData):
    """
    Model for the sensor data sent by the RAK node through the API
    """
    alarm: bool = Field(..., description="Indicates if the node has turned the alarm on.")
