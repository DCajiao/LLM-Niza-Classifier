import { motion } from "framer-motion";
import Swal from "sweetalert2";

const Step2 = ({ formData, setFormData, onNext, onBack }) => {
    const handleChange = (e) => {
        setFormData({ ...formData, [e.target.name]: e.target.value });
    };
    const handleValidation = () => {
        const { carrera, semestre, experiencia_previa } = formData;
    
        if (!carrera || !semestre || !experiencia_previa) {
            Swal.fire("Campos incompletos", "Por favor completa todos los campos antes de continuar.", "warning");
            return;
        }
    
        onNext();
    };

    return (
        <motion.div
            className="bg-white rounded-2xl shadow-md p-6 w-full max-w-3xl mx-auto"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
        >
        <div>
            <h2 className="text-xl font-bold mb-4">Paso 2: Información Académica</h2>
            <div className="mb-4">
                <label className="block mb-1">Carrera:</label>
                <input
                    type="text"
                    name="carrera"
                    value={formData.carrera || ""}
                    onChange={handleChange}
                    className="border p-2 w-full"
                />
            </div>
            <div className="mb-4">
                <label className="block mb-1">Semestre:</label>
                <input
                    type="text"
                    name="semestre"
                    value={formData.semestre || ""}
                    onChange={handleChange}
                    className="border p-2 w-full"
                />
            </div>
            <div className="mb-4">
                <label className="block mb-1">¿Tienes experiencia previa emprendiendo?</label>
                <select
                    name="experiencia_previa"
                    value={formData.experiencia_previa || ""}
                    onChange={handleChange}
                    className="border p-2 w-full"
                >
                    <option value="">Selecciona una opción</option>
                    <option value="Sí">Sí</option>
                    <option value="No">No</option>
                </select>
            </div>

            <div className="flex justify-between">
                <button onClick={onBack} className="btn btn-secondary me-2">Anterior</button>
                <button onClick={handleValidation} className="btn btn-primary">Siguiente</button>
            </div>
        </div>
        </motion.div>
    );
};

export default Step2;
