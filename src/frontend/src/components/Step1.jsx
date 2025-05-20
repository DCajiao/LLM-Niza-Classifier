import { motion } from "framer-motion";
import Swal from "sweetalert2";

export default function Step1({ formData, setFormData, onNext }) {
  const handleValidation = () => {
    const { nombre, email, edad, universidad } = formData;

    // Si la edad no es nula y es mayor a 18, entonces se puede continuar
    if (edad && edad < 18) {
      Swal.fire("Edad inválida", "Debes tener al menos 18 años para registrarte.", "warning");
      console.log(formData);
      return;
    }

    if (!universidad) {
      Swal.fire("Campos incompletos", "Por favor completa todos los campos antes de continuar.", "warning");
      return;
    }

    onNext();
  };

  const universidades = [
    "Universidad",
    "UAO",
  ];

  return (
    <motion.div
      className="bg-white rounded-2xl shadow-md p-6 w-full max-w-3xl mx-auto"
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
    >
    <div className="bg-white p-6 rounded-md shadow-md">
      <h2 className="text-xl font-bold text-indigo-700 mb-4">Paso 1: Información Personal</h2>
        <div className="grid gap-4 md:grid-cols-2">
          <input type="number" placeholder="Edad (Opcional)" value={formData.edad} onChange={e => setFormData({ ...formData, edad: e.target.value })} className="p-2 border rounded" />
          <select
            value={formData.universidad}
            onChange={e => setFormData({ ...formData, universidad: e.target.value })}
            className="p-2 border rounded"
          >
            {universidades.map((uni, index) => (
              <option key={index} value={index === 0 ? "" : uni} disabled={index === 0}>
                {uni}
              </option>
            ))}
          </select>
        </div>
      <button onClick={handleValidation} className="btn btn-primary">Siguiente</button>
    </div>
    </motion.div>
  );
}
