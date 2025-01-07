import React, { useEffect, useState } from "react";
import { Line } from "react-chartjs-2";
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
} from "chart.js";

// Registrar los componentes de Chart.js que vamos a usar
ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
);

const Graph = ({ sensorData }) => {
  const [chartData, setChartData] = useState(null);

  // Formatear los datos del sensor para que los gráficos puedan ser generados
  useEffect(() => {
    if (sensorData && sensorData.length > 0) {
      const labels = sensorData[0].data.map((data) => data.timestamp); // Usamos los timestamps del primer sensor
      const datasets = sensorData.map((sensor) => {
        const temperatureData = sensor.data.map((data) => data.temperature);
        const humidityData = sensor.data.map((data) => data.humidity);
        
        return [
          {
            label: `${sensor.sensor.name} - Temperature (°C)`,
            data: temperatureData,
            borderColor: "rgba(255, 99, 132, 1)",
            backgroundColor: "rgba(255, 99, 132, 0.2)",
            fill: false
          },
          {
            label: `${sensor.sensor.name} - Humidity (%)`,
            data: humidityData,
            borderColor: "rgba(54, 162, 235, 1)",
            backgroundColor: "rgba(54, 162, 235, 0.2)",
            fill: false
          }
        ];
      }).flat(); // Aplanar el array para obtener todos los datasets

      // Crear la estructura de datos para Chart.js
      setChartData({
        labels: labels,
        datasets: datasets
      });
    }
  }, [sensorData]);

  // Verificar si los datos aún no se han cargado
  if (!chartData) {
    return <p>Loading graph...</p>;
  }

  return (
    <div>
      <h2>Sensor Data Graph</h2>
      <Line data={chartData} />
    </div>
  );
};

export default Graph;
