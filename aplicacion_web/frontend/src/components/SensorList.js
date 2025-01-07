import React, { useState, useEffect } from 'react';
import SensorCard from "./SensorCard";
import Graph from "./Graph";

const SensorList = ({ sensors }) => {
  const [selectedSensors, setSelectedSensors] = useState([]);
  const [sensorData, setSensorData] = useState([]);

  const handleSelectSensor = (sensor) => {
    setSelectedSensors((prev) => {
      if (prev.some((s) => s.id === sensor.id)) {
        return prev.filter((s) => s.id !== sensor.id);
      }
      return [...prev, sensor];
    });
  };

  const fetchSensorData = async () => {
    const data = [];
    for (const sensor of selectedSensors) {
      const response = await fetch(`http://localhost:8000/sensor_data/${sensor.id}/`);
      const sensorData = await response.json();
      data.push({ sensor, data: sensorData });
    }
    setSensorData(data);
  };

  return (
    <div>
      <div className="sensor-cards">
        {sensors.map((sensor) => (
          <SensorCard 
            key={sensor.id} 
            sensor={sensor} 
            onSelect={handleSelectSensor} 
            isSelected={selectedSensors.some(s => s.id === sensor.id)} 
          />
        ))}
      </div>

      <button 
        onClick={fetchSensorData} 
        disabled={selectedSensors.length === 0}
      >
        Generate Graph
      </button>

      {sensorData.length > 0 && <Graph sensorData={sensorData} />}
    </div>
  );
};

export default SensorList;
