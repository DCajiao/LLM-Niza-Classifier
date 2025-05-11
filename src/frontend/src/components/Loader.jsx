import React from "react";
import "../styles/Loader.css";

const Loader = () => {
  return (
    <div className="loader-overlay">
      <div className="loader-spinner"></div>
      <p className="loader-text">Nuestra IA está procesando tu solicitud... Por favor espera</p>
    </div>
  );
};

export default Loader;
