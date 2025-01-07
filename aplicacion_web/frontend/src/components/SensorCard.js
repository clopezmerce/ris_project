import React from "react";
import "../styles/SensorCard.css"

const SensorCard = ({ sensor, onSelect, isSelected }) => {
  return (
    <div
      className={`sensor-card ${isSelected ? "selected" : ""}`} // Añadir clase "selected" si está seleccionado
      onClick={() => onSelect(sensor)}
    >
      <h3>{sensor.name}</h3>
    </div>
  );
};

export default SensorCard;
