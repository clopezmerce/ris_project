import React from 'react';

const SensorCard = ({ sensorId, onToggle, isSelected }) => (
  <div
    style={{
      border: '1px solid #ccc',
      padding: '10px',
      margin: '10px',
      backgroundColor: isSelected ? '#d1e7dd' : '#fff',
      cursor: 'pointer',
    }}
    onClick={() => onToggle(sensorId)}
  >
    <h3>Sensor: {sensorId}</h3>
    <p>Click para {isSelected ? 'deseleccionar' : 'seleccionar'}</p>
  </div>
);

export default SensorCard;
