import { motion } from "framer-motion";

export default function Sidebar({ step, setStep }) {
  const steps = [
    "Datos personales",
    "Formación académica",
    "Emprendimiento",
    "Clasificación",
    "Resumen",
  ];

  return (
    <motion.div
      className="bg-white rounded-2xl shadow-md p-6 w-full max-w-3xl mx-auto"
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
    >
      <aside className="sidebar">
      <img src={`${import.meta.env.BASE_URL}img/icon_without_background.png`} alt="icono" />
        <h2>Progreso</h2>
        <ul>
          {steps.map((label, index) => (
            <li key={index} className={step === index + 1 ? "active" : ""}>
              Paso {index + 1}: {label}
            </li>
          ))}
        </ul>
        <hr></hr>
        <div className="text-center grid gap-4">
            <button onClick={() => setStep(6)} className="btn btn-primary mt-3 w-100">
              Dashboard en Tiempo Real
            </button>
        </div>
      </aside>
    </motion.div>
  );
}
