import React, { useState, useEffect } from 'react';
import SensorList from './components/SensorList';
import Graph from './components/Graph';
import ApiService from './services/ApiService';

const App = () => {
  const [sensors, setSensors] = useState([]);
  const [selectedSensors, setSelectedSensors] = useState([]);

  useEffect(() => {
    console.log("Haciendo la llamada a la API")
    ApiService.getSensors().then(data => {
      console.log("Datos de sensores recibidos:", data)
      setSensors(data.sensors)
    });
  }, []);

  const toggleSensorSelection = (sensorId) => {
    setSelectedSensors(prev =>
      prev.includes(sensorId) ? prev.filter(id => id !== sensorId) : [...prev, sensorId]
    );
  };

  return (
    <div>
      <h1>Sensor Dashboard</h1>
      <SensorList sensors={sensors} onToggle={toggleSensorSelection} />
      {selectedSensors.length > 0 && <Graph sensors={selectedSensors} />}
    </div>
  );
};

export default App;
