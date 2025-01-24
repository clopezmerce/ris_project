import React, { useState, useEffect } from 'react';
import DatePicker from 'react-datepicker';
import 'react-datepicker/dist/react-datepicker.css';
import SensorList from './components/SensorList';
import Graph from './components/Graph';
import ApiService from './services/ApiService';

const App = () => {
  const [sensors, setSensors] = useState([]); // IDs de sensores disponibles
  const [selectedSensors, setSelectedSensors] = useState([]); // IDs seleccionados
  const [sensorData, setSensorData] = useState([]); // Datos de sensores para la gráfica
  const [startDate, setStartDate] = useState(null);
  const [endDate, setEndDate] = useState(null);

  // Cargar los IDs de los sensores al inicio
  useEffect(() => {
    ApiService.getSensors().then(data => setSensors(data.sensors, data.startDate, data.endDate));
  }, []);

  // Función para seleccionar o deseleccionar sensores
  const toggleSensorSelection = (sensorId) => {
    setSelectedSensors(prev =>
      prev.includes(sensorId) ? prev.filter(id => id !== sensorId) : [...prev, sensorId]
    );
  };

  // Función para obtener datos y generar la gráfica
  const handleGenerateGraph = async () => {
    const startTime = startDate ? startDate.toISOString() : null;
    const endTime = endDate ? endDate.toISOString() : null;

    const dataPromises = selectedSensors.map(sensorId =>
      ApiService.getSensorData(sensorId, startTime, endTime)
    );
    const sensorResults = await Promise.all(dataPromises);
    
    setSensorData(sensorResults.map((data, index) => ({
      sensorId: selectedSensors[index],
      readings: data, // Suponiendo que la API devuelve una lista de lecturas con timestamp
    })));
  };

  return (
    <div>
      <h1>Sensor Dashboard</h1>
      <SensorList sensors={sensors} selectedSensors={selectedSensors} onToggle={toggleSensorSelection} />
      <div style={{ marginBottom: '20px' }}>
        <label>Desde: </label>
        <DatePicker selected={startDate} onChange={setStartDate} dateFormat="yyyy-MM-dd HH:mm" showTimeSelect />
        <label> Hasta: </label>
        <DatePicker selected={endDate} onChange={setEndDate} dateFormat="yyyy-MM-dd HH:mm" showTimeSelect />
      </div>
      <button onClick={handleGenerateGraph} disabled={selectedSensors.length === 0}>
        Generar Gráficas
      </button>
      {sensorData.length > 0 && <Graph sensorData={sensorData} />}
    </div>
  );
};

export default App;
