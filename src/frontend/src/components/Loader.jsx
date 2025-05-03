import React from "react";
import "../styles/Loader.css"; // estilos separados para mejor organización

const Loader = () => {
  return (
    <div className="loader-overlay">
      <div className="loader-spinner"></div>
      <p className="loader-text">Procesando... Por favor espera</p>
    </div>
  );
};

export default Loader;
