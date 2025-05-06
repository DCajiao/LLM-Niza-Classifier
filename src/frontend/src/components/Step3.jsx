import React from "react";
import { motion } from "framer-motion";

const Step3 = ({ formData, setFormData, onNext, onBack }) => {
  const isValid =
    formData.nombre_emprendimiento.trim() !== "" &&
    formData.descripcion_emprendimiento.trim().length >= 50;

  return (
    <motion.div
      className="bg-white rounded-2xl shadow-md p-6 w-full max-w-3xl mx-auto"
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
    >
      <h2 className="text-xl font-semibold text-indigo-700 mb-4">
        Paso 3: Información del Emprendimiento
      </h2>
      <p className="text-gray-600 mb-6">
        Cuéntanos sobre tu proyecto o idea de negocio.
      </p>

      <div className="mb-5">
        <label className="block font-medium text-gray-700 mb-1">
          Nombre del Emprendimiento *
        </label>
        <input
          type="text"
          className="w-full border border-gray-300 rounded-md px-4 py-2 focus:outline-none focus:ring-2 focus:ring-indigo-500"
          value={formData.nombre_emprendimiento}
          onChange={(e) =>
            setFormData({ ...formData, nombre_emprendimiento: e.target.value })
          }
          placeholder="Ej. EcoSolutions, TechInnovate, etc."
        />
      </div>

      <div className="mb-5">
        <label className="block font-medium text-gray-700 mb-1">
          Descripción detallada del emprendimiento *
        </label>
        <textarea
          className="w-full border border-gray-300 rounded-md px-4 py-2 focus:outline-none focus:ring-2 focus:ring-indigo-500"
          value={formData.descripcion_emprendimiento}
          onChange={(e) =>
            setFormData({ ...formData, descripcion_emprendimiento: e.target.value })
          }
          rows="6"
          placeholder="Describe con detalle los productos o servicios, público objetivo, canales de distribución, etc."
        ></textarea>
        <p
          className={`text-sm mt-1 text-right ${
            formData.descripcion_emprendimiento.length >= 50
              ? "text-green-600"
              : "text-red-500"
          }`}
        >
          {formData.descripcion_emprendimiento.length}/50 caracteres mínimos
        </p>
      </div>

      <div className="flex justify-between mt-6">
        <button
          className="btn btn-secondary me-2"
          onClick={onBack}
        >
          ← Anterior
        </button>
        <button
          className={`btn btn-primary transition-colors duration-200 ${
            isValid
              ? "bg-indigo-600 hover:bg-indigo-700"
              : "bg-gray-400 cursor-not-allowed"
          }`}
          onClick={onNext}
          disabled={!isValid}
        >
          Continuar →
        </button>
      </div>
    </motion.div>
  );
};

export default Step3;