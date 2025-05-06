import React from "react";
import "../styles/Loader.css"; // estilos separados para mejor organización

const Loader = () => {
  return (
    <div className="loader-overlay">
      <div className="loader-spinner"></div>
      <p className="loader-text">Nuestra IA está procesando tu solicitud... Por favor espera</p>
    </div>
  );
};

export default Loader;
