import React, { useState, useEffect } from 'react';
import ApiService from '../services/ApiService';

const StatusPage = () => {
  const [sensorStatus, setSensorStatus] = useState({});
  const [alarmActive, setAlarmActive] = useState(false);

  useEffect(() => {
    const fetchSensorStatus = async () => {
      const data = await ApiService.getSensorStatus();
      setSensorStatus(data);
      setAlarmActive(data["rak_alarm"]);
    };

    fetchSensorStatus();
  }, []);

  const handleTurnOffAlarm = async () => {
    await ApiService.turnOffLed();
    setAlarmActive(false);
  };

  return (
    <div className="container mt-4">
      <div className="p-4">
        <h2 className="text-center mb-4">Estado de los Sensores</h2>

        {/* Tabla de estados */}
        <table className="table table-striped table-bordered">
          <thead className="table-dark">
            <tr>
              <th>ID del Sensor</th>
              <th>Estado</th>
            </tr>
          </thead>
          <tbody>
            {Object.entries(sensorStatus).map(([sensorId, isActive]) =>
              sensorId !== "rak_alarm" ? (
                <tr key={sensorId}>
                  <td>{sensorId}</td>
                  <td className="text-center">
                    {isActive ? '🟢 Activo' : '🔴 Inactivo'}
                  </td>
                </tr>
              ) : null
            )}
          </tbody>
        </table>

        {/* Botón para apagar la alarma si está activa */}
        {alarmActive && (
          <div className="text-center mt-3">
            <button className="btn btn-danger btn-lg" onClick={handleTurnOffAlarm}>
              Apagar Alarma
            </button>
          </div>
        )}
      </div>
    </div>
  );
};

export default StatusPage;
