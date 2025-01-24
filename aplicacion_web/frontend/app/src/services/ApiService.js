const API_BASE_URL = 'http://localhost:8000'; // Cambiar según corresponda

const ApiService = {
  getSensors: async () => {
    const response = await fetch(`${API_BASE_URL}/sensors/`);
    return response.json();
  },
  getSensorData: async (sensorId, startTime, endTime) => {
    const url = new URL(`${API_BASE_URL}/sensor_data/${sensorId}/`);
    if (startTime) url.searchParams.append('start_time', startTime);
    if (endTime) url.searchParams.append('end_time', endTime);

    const response = await fetch(url);
    return response.json();
  },
};

export default ApiService;
