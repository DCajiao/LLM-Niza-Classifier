import { motion } from "framer-motion";
import Swal from "sweetalert2";

const Step2 = ({ formData, setFormData, onNext, onBack }) => {
    const handleChange = (e) => {
        const { name, value } = e.target;

        // If the category changes, reset the carrera field
        if (name === "categoriaCarrera") {
        setFormData({ ...formData, categoriaCarrera: value, carrera: "" });
        } else {
        setFormData({ ...formData, [name]: value });
        }
    };
    const handleValidation = () => {
        const { carrera, semestre, experiencia_previa } = formData;

        if (semestre < 1 || semestre > 16) {
            Swal.fire("Semestre inválido", "El semestre debe estar entre 1 y 16.", "warning");
            return;
        }

        if (!carrera || !semestre || !experiencia_previa) {
            Swal.fire("Campos incompletos", "Por favor completa todos los campos antes de continuar.", "warning");
            return;
        }
    
        console.log(formData);
        onNext();
    };

    const carrers = {
        "Ingeniería y Ciencias Básicas": [
            "Ingeniería de Datos e Inteligencia Artificial",
            "Ingeniería Multimedia",
            "Ingeniería Informática",
            "Ingeniería Industrial",
            "Ingeniería Eléctrica",
            "Ingeniería Mecatrónica",
            "Ingeniería Mecánica",
            "Ingeniería Biomédica",
            "Ingeniería Ambiental",
            "Ingeniería y Ciencias Básicas",],
        "Administración": [
            "Publicidad en Medios Digitales",
            "Mercadeo y Negocios Internacionales",
            "Administración de Empresas - Modelo Dual",
            "Mercadeo Global",
            "Contaduría Pública",
            "Derecho",],
        "Arquitectura, Urbanismo y Diseño": [
            "Arquitectura",
            "Diseño de la Comunicación Gráfica",],
        "Comunicación Social, Humanidades y Artes": [
            "Cine",
            "Comunicación Social - Periodismo",
            "Narrativas y Entretenimiento Digital",],
    }

    const categorias = Object.keys(carrers);
    const carrersFiltradas = carrers[formData.categoriaCarrera] || [];

    return (
        <motion.div
            className="bg-white rounded-2xl shadow-md p-6 w-full max-w-3xl mx-auto"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
        >
        <div>
            <h2 className="text-xl font-bold mb-4">Paso 2: Información Académica</h2>
            <div className="mb-4">
                <label className="block mb-1">Área académica:</label>
                <select
                    name="categoriaCarrera"
                    value={formData.categoriaCarrera || ""}
                    onChange={handleChange}
                    className="border p-2 w-full"
                >
                    <option value="">Selecciona un área</option>
                    {categorias.map((cat, idx) => (
                    <option key={idx} value={cat}>{cat}</option>
                    ))}
                </select>
            </div>
            {formData.categoriaCarrera && (
            <div className="mb-4">
                <label className="block mb-1">Carrera:</label>
                <select
                name="carrera"
                value={formData.carrera || ""}
                onChange={handleChange}
                className="border p-2 w-full"
                >
                <option value="">Selecciona una carrera</option>
                {carrersFiltradas.map((carrera, idx) => (
                    <option key={idx} value={carrera}>{carrera}</option>
                ))}
                </select>
            </div>
            )}
            <div className="mb-4">
                <label className="block mb-1">Semestre:</label>
                <input
                    type="number"
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
