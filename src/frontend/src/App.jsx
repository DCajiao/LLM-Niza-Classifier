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

  const handleNext = () => setStep((prev) => Math.min(prev + 1, 5));
  const handleBack = () => setStep((prev) => Math.max(prev - 1, 1));

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
      default:
        return <div>¡Gracias por participar!</div>;
    }
  };

  return (
    <Router>
      <div className="min-vh-100 bg-light">
        <Header />
        <div className="d-flex app-container p-4">
          <Sidebar step={step} />
          <main className="main-content">
            <div className="card shadow-sm p-4">
              <Routes>
                <Route path="/" element={renderStep()} />
                <Route path="/dashboard" element={<Dashboard />} />
              </Routes>
            </div>
          </main>
        </div>
        <Footer />
      </div>
    </Router>
  );
}
