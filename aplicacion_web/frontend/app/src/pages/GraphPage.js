import React, { useState, useEffect } from 'react';
import DatePicker from 'react-datepicker';
import 'react-datepicker/dist/react-datepicker.css';
import { Button, Container, Row, Col, Card } from 'react-bootstrap';
import SensorList from '../components/SensorList';
import Graph from '../components/Graph';
import ApiService from '../services/ApiService';

const GraphPage = () => {
  const [sensors, setSensors] = useState([]);
  const [selectedSensors, setSelectedSensors] = useState([]);
  const [sensorData, setSensorData] = useState([]);
  const [startDate, setStartDate] = useState(null);
  const [endDate, setEndDate] = useState(null);

  useEffect(() => {
    ApiService.getSensors().then(data => setSensors(data.sensors));
  }, []);

  const toggleSensorSelection = (sensorId) => {
    setSelectedSensors(prev =>
      prev.includes(sensorId) ? prev.filter(id => id !== sensorId) : [...prev, sensorId]
    );
  };

  const handleGenerateGraph = async () => {
    const startTime = startDate ? startDate.toISOString() : null;
    const endTime = endDate ? endDate.toISOString() : null;

    const dataPromises = selectedSensors.map(sensorId =>
      ApiService.getSensorData(sensorId, startTime, endTime)
    );
    const sensorResults = await Promise.all(dataPromises);

    setSensorData(sensorResults.map((data, index) => ({
      sensorId: selectedSensors[index],
      readings: data,
    })));
  };

  return (
    <Container>
      <h1 className="text-center my-4">Gráficas de Sensores</h1>

      {/* Selección de Sensores y Filtros */}
      <Row>
        <Col md={6}>
          <Card className="p-3 mb-3">
            <h5 className="mb-3">Selecciona Sensores</h5>
            <SensorList sensors={sensors} selectedSensors={selectedSensors} onToggle={toggleSensorSelection} />
          </Card>
        </Col>

        <Col md={6}>
          <Card className="p-3 mb-3">
            <h5 className="mb-3">Selecciona Rango de Fechas</h5>
            <div className="mb-3">
              <label className="fw-bold">Desde: </label>
              <DatePicker
                selected={startDate}
                onChange={setStartDate}
                dateFormat="yyyy-MM-dd HH:mm"
                showTimeSelect
                className="form-control px-2"
              />
            </div>
            <div className="mb-3">
              <label className="fw-bold">Hasta: </label>
              <DatePicker
                selected={endDate}
                onChange={setEndDate}
                dateFormat="yyyy-MM-dd HH:mm"
                showTimeSelect
                className="form-control px-2"
              />
            </div>
          </Card>
        </Col>
      </Row>

      {/* Botón para Generar Gráficas */}
      <div className="text-center mb-4">
        <Button onClick={handleGenerateGraph} disabled={selectedSensors.length === 0} variant="primary">
          Generar Gráficas
        </Button>
      </div>

      {/* Gráfica */}
      {sensorData.length > 0 && <Graph sensorData={sensorData} />}
    </Container>
  );
};

export default GraphPage;
