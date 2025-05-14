import { motion } from "framer-motion";
import Swal from "sweetalert2";

export default function Step1({ formData, setFormData, onNext }) {
  const handleValidation = () => {
    const { nombre, email, edad, universidad } = formData;

    if (edad < 18) {
      Swal.fire("Edad inválida", "Debes tener al menos 18 años para registrarte.", "warning");
      return;
    }

    if (!nombre || !email || !edad || !universidad) {
      Swal.fire("Campos incompletos", "Por favor completa todos los campos antes de continuar.", "warning");
      return;
    }

    const emailRegex = /\S+@\S+\.\S+/;
    if (!emailRegex.test(email)) {
      Swal.fire("Correo inválido", "Ingresa un correo electrónico válido.", "warning");
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
    <div className="bg-white p-6 rounded-md shadow-md">
      <h2 className="text-xl font-bold text-indigo-700 mb-4">Paso 1: Información Personal</h2>
      <div className="grid gap-4 md:grid-cols-2">
        <input type="text" placeholder="Nombre completo" value={formData.nombre} onChange={e => setFormData({...formData, nombre: e.target.value})} className="p-2 border rounded" />
        <input type="email" placeholder="Correo electrónico" value={formData.email} onChange={e => setFormData({...formData, email: e.target.value})} className="p-2 border rounded" />
        <input type="number" placeholder="Edad" value={formData.edad} onChange={e => setFormData({...formData, edad: e.target.value})} className="p-2 border rounded" />
        <input type="text" placeholder="Universidad" value={formData.universidad} onChange={e => setFormData({...formData, universidad: e.target.value})} className="p-2 border rounded" />
      </div>
      <button onClick={handleValidation} className="btn btn-primary">Siguiente</button>
    </div>
    </motion.div>
  );
}
