import React from 'react';
import { Line } from 'react-chartjs-2';
import { Chart, registerables } from 'chart.js';
import 'chartjs-adapter-date-fns';

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
        type: 'time', // Ahora funcionará correctamente
        time: {
          unit: 'minute',
          tooltipFormat: 'yyyy-MM-dd HH:mm',
          displayFormats: {
            minute: 'dd/MM HH:mm',
          },
        },
        title: { display: true, text: 'Fecha y Hora' },
      },
      y: { title: { display: true, text: 'Valor' } },
    },
  };

  // Datos para temperatura
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

  // Datos para humedad
  const humData = {
    datasets: sensorData.map((sensor, index) => ({
      label: `Hum - Sensor ${sensor.sensorId}`,
      data: sensor.readings.map(d => ({
        x: new Date(d.timestamp),
        y: d.humidity,
      })),
      borderColor: colors[index % colors.length],
      borderDash: [5, 5], // Línea punteada para humedad
      fill: false,
    })),
  };

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '20px', alignItems: 'center' }}>
      <div style={{ width: '700px', height: '300px' }}>
        <h2>Temperatura</h2>
        <Line data={tempData} options={commonOptions} />
      </div>
      <div style={{ width: '700px', height: '300px' }}>
        <h2>Humedad</h2>
        <Line data={humData} options={commonOptions} />
      </div>
    </div>
  );
};

export default Graph;
