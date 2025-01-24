import React from 'react';
import SensorCard from './SensorCard';

const SensorList = ({ sensors, selectedSensors, onToggle }) => (
  <div style={{ display: 'flex', flexWrap: 'wrap' }}>
    {sensors.map(sensor => (
      <SensorCard
        key={sensor}
        sensorId={sensor}
        onToggle={onToggle}
        isSelected={selectedSensors.includes(sensor)}
      />
    ))}
  </div>
);

export default SensorList;
