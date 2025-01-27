import React from 'react';
import { Line } from 'react-chartjs-2';
import { Chart, registerables } from 'chart.js';
import 'chartjs-adapter-date-fns';
import 'bootstrap/dist/css/bootstrap.min.css';

Chart.register(...registerables);

const Graph = ({ sensorData }) => {
  const colors = ['red', 'blue', 'green', 'orange', 'purple', 'brown', 'pink'];

  const commonOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: { position: 'top' },
    },
    scales: {
      x: {
        type: 'time',
        time: {
          unit: 'minute',
          tooltipFormat: 'yyyy-MM-dd HH:mm',
          displayFormats: { minute: 'dd/MM HH:mm' },
        },
        title: { display: true, text: 'Fecha y Hora' },
      },
      y: { title: { display: true, text: 'Valor' } },
    },
  };

  // Temperatura
  const tempData = {
    datasets: sensorData.map((sensor, index) => ({
      label: `Temp - Sensor ${sensor.sensorId}`,
      data: sensor.readings.map(d => ({
        x: new Date(d.timestamp),
        y: d.temperature,
      })),
      borderColor: colors[index % colors.length],
      fill: false,
    })),
  };

  // Humedad
  const humData = {
    datasets: sensorData.map((sensor, index) => ({
      label: `Hum - Sensor ${sensor.sensorId}`,
      data: sensor.readings.map(d => ({
        x: new Date(d.timestamp),
        y: d.humidity,
      })),
      borderColor: colors[index % colors.length],
      borderDash: [5, 5],
      fill: false,
    })),
  };

  return (
    <div className="container mt-4">
      <div className="row g-4">
        <div className="col-lg-6 col-12">
          <div className="card p-3 shadow">
            <h4 className="text-center">Temperatura</h4>
            <div className="chart-container" style={{ height: '300px' }}>
              <Line data={tempData} options={commonOptions} />
            </div>
          </div>
        </div>

        <div className="col-lg-6 col-12">
          <div className="card p-3 shadow">
            <h4 className="text-center">Humedad</h4>
            <div className="chart-container" style={{ height: '300px' }}>
              <Line data={humData} options={commonOptions} />
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Graph;
