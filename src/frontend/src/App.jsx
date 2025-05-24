import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Header from "./components/Header";
import Sidebar from "./components/Sidebar";
import Step1 from "./components/Step1";
import Step2 from "./components/Step2";
import Step3 from "./components/Step3";
import Step4 from "./components/Step4";
import Dashboard from "./components/Dashboard";
import Footer from "./components/Footer";
import { useEffect, useState } from "react";

export default function App() {
  const [step, setStep] = useState(1);

  // Inicialization of formData from localStorage if it exists
  const [formData, setFormData] = useState(() => {
    const savedData = localStorage.getItem("formData");
    return savedData
      ? JSON.parse(savedData)
      : {
          nombre: "",
          email: "",
          edad: "",
          universidad: "",
          carrera: "",
          semestre: "",
          experiencia_previa: "",
          nombre_emprendimiento: "",
          descripcion_emprendimiento: "",
          acepta_politica: false,
        };
  });

  // Persist automatically in localStorage each time formData changes
  useEffect(() => {
    localStorage.setItem("formData", JSON.stringify(formData));
  }, [formData]);

  const handleNext = () => setStep((prev) => Math.min(prev + 1, 6));
  const handleBack = () => setStep((prev) => Math.max(prev - 1, 1));
  const handleReset = () => {setStep(1)};

  const renderStep = () => {
    switch (step) {
      case 1:
        return <Step1 formData={formData} setFormData={setFormData} onNext={handleNext} />;
      case 2:
        return <Step2 formData={formData} setFormData={setFormData} onNext={handleNext} onBack={handleBack} />;
      case 3:
        return <Step3 formData={formData} setFormData={setFormData} onNext={handleNext} onBack={handleBack} />;
      case 4:
        return <Step4 formData={formData} setFormData={setFormData} onNext={handleNext} onBack={handleBack} />;
      case 5:
        return (
          <div className="text-center grid gap-4">
            <h2 className="text-2xl font-bold mb-4">¡Gracias por completar el formulario!</h2>
            <p className="mb-4">Tu información ha sido guardada exitosamente.</p>
            <button onClick={handleReset} className="btn btn-primary">
              Volver a empezar
            </button>
            <button onClick={() => setStep(6)} className="btn btn-secondary ml-2">
              Ir al Dashboard
            </button>
          </div>
        );
      case 6:
        return <Dashboard handleReset={handleReset}/>;
      default:
        return <Step1 formData={formData} setFormData={setFormData} onNext={handleNext} />;
    }
  };

  return (
    <Router>
      <div className="min-vh-100 bg-light">
        <Header />
        <div className="d-flex app-container p-4">
          <Sidebar step={step} setStep={setStep} />
          <main className="main-content">
            <div className="card shadow-sm p-4">
              <Routes>
                <Route path="/" element={renderStep()} />
              </Routes>
            </div>
          </main>
        </div>
        <Footer />
      </div>
    </Router>
  );
}
