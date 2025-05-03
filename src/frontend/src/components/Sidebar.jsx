// src/components/Sidebar.jsx
export default function Sidebar({ step }) {
  const steps = [
    "Datos personales",
    "Formación académica",
    "Emprendimiento",
    "Clasificación",
    "Resumen"
  ];

  return (
    <aside className="sidebar">
      <h2>Progreso</h2>
      <ul>
        {steps.map((label, index) => (
          <li key={index} className={step === index + 1 ? "active" : ""}>
            Paso {index + 1}: {label}
          </li>
        ))}
      </ul>
    </aside>
  );
}
