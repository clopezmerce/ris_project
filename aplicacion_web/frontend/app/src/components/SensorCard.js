import React from 'react';

const SensorCard = ({ sensorId, isSelected, onToggle }) => {
  return (
    <div 
      className={`card p-3 shadow-sm ${isSelected ? 'border-primary' : ''}`} 
      style={{ width: '200px', cursor: 'pointer' }} 
      onClick={() => onToggle(sensorId)}
    >
      <div className="card-body text-center d-flex align-items-center justify-content-center h-100">
        <h6 className="card-title fw-bold text-wrap w-100" style={{ wordBreak: 'break-word' }}>
          {sensorId}
        </h6>
      </div>
    </div>
  );
};

export default SensorCard;
