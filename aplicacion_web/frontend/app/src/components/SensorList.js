import React from 'react';
import SensorCard from './SensorCard';

const SensorList = ({ sensors, selectedSensors, onToggle }) => (
  <div className="d-flex flex-wrap gap-3 mx-2">
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
