import React, { useState } from "react";
import Header from "./components/Header";
import Sidebar from "./components/Sidebar";
import Step1 from "./components/Step1";
import Step2 from "./components/Step2";
import Step3 from "./components/Step3";
import Step4 from "./components/Step4";

export default function App() {
    const [step, setStep] = useState(1);

    const [formData, setFormData] = useState({
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
    });

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
            case 5:
                return <Dashboard />;

            default:
                return <div>¡Gracias por participar!</div>;
        }
    };

    return (
        <div className="min-vh-100 bg-light py-4">
          <Header />
          <div className="container">
            <div className="row">
              <div className="col-md-4">
                <Sidebar step={step} />
              </div>
              <div className="col-md-8">
                <div className="card shadow-sm p-4">
                  {renderStep()}
                </div>
              </div>
            </div>
          </div>
        </div>
      );
      
}
