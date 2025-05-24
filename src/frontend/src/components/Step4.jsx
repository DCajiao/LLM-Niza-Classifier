import { useEffect, useState } from "react";
import Swal from "sweetalert2";
import { obtenerClasificacionNiza } from "../services/llmService";
import { guardarRegistro } from "../services/backendService";
import Loader from "../components/Loader";
import { motion } from "framer-motion";

export default function Paso4Clasificacion({ formData, setFormData, onNext, onBack }) {
    const [clasificaciones, setClasificaciones] = useState(null);
    const [loading, setLoading] = useState(false);

    const procesarClasificacion = async () => {
        setLoading(true);
        try {
            const response = await obtenerClasificacionNiza(formData.descripcion_emprendimiento);
            //console.log("Clasificaciones obtenidas:", response);
            setClasificaciones(response.clasificaciones);
            setFormData((prev) => ({ ...prev, clasificaciones_niza: response.clasificaciones }));
            Swal.fire("Clasificación completada", "Se han generado recomendaciones", "success");
        } catch (err) {
            console.error("Error al obtener clasificaciones:", err);
            Swal.fire("Error", "Hubo un problema al obtener las clasificaciones", "error");
        }
        setLoading(false);
    };

    const enviarFinal = async () => {
        if (!formData.acepta_politica) {
            Swal.fire("Campo obligatorio", "Debes aceptar la política de privacidad", "warning");
            return;
        }
        
        setLoading(true);

        try {
            console.log("Datos a guardar:", formData);
            await guardarRegistro(formData);
            Swal.fire("Registro exitoso", "Tus datos han sido almacenados", "success");

            setFormData({...formData,
                nombre_emprendimiento: "",
                descripcion_emprendimiento: "",
                clasificaciones_niza: [],
                acepta_politica: false,
            });
            
            onNext();
        } catch (e) {
            Swal.fire("Error", "No se pudo guardar tu información", "error");
        }
    };

    useEffect(() => {
        if (!clasificaciones) {
            //console.log("Descripción del emprendimiento:", formData.descripcion_emprendimiento);

            let isCancelled = false;

            const clasificar = async () => {
                setLoading(true);
                try {
                    const response = await obtenerClasificacionNiza(formData.descripcion_emprendimiento);
                    if (!isCancelled) {
                        //console.log("Clasificaciones obtenidas:", response);
                        setClasificaciones(response.clasificaciones);
                        setFormData((prev) => ({
                            ...prev,
                            clasificaciones_niza: response.clasificaciones,
                        }));
                        Swal.fire("Clasificación completada", "Se han generado recomendaciones", "success");
                    }
                } catch (err) {
                    if (!isCancelled) {
                        console.error("Error al obtener clasificaciones:", err);
                        Swal.fire("Error", "Hubo un problema al obtener las clasificaciones", "error");
                    }
                }
                setLoading(false);
            };

            clasificar();

            return () => {
                isCancelled = true; // evita que setState corra dos veces
            };
        }
    }, []);

    return (
        <motion.div
              className="bg-white rounded-2xl shadow-md p-6 w-full max-w-3xl mx-auto"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
        >
        <div className="card">
            <h2>Paso 4: Clasificación Niza</h2>
            <p className="text-gray">Recomendaciones basadas en la descripción del emprendimiento.</p>
            {loading && <Loader mensaje="Clasificando tu emprendimiento..." />}

            {!loading && clasificaciones && (
                <>
                    <h3>Clasificaciones sugeridas:</h3>
                    <ul className="niza-list">
                        {clasificaciones.map((c, idx) => (
                            <li key={idx} className="niza-item">
                                <strong>Clase {c.clase}:</strong> {c.descripcion}<br />
                                <small>Confianza: {c.confianza}% | Relevancia: {c.relevancia || "N/A"}</small>
                            </li>
                        ))}
                    </ul>

                    <div className="d-flex align-items-start gap-2 my-3">
                        <input
                            className="form-check-input mt-1"
                            type="checkbox"
                            id="acepta"
                            checked={formData.acepta_politica}
                            onChange={(e) =>
                            setFormData({ ...formData, acepta_politica: e.target.checked })
                            }
                        />
                        <label htmlFor="acepta" className="form-check-label">
                            Acepto la <a href="https://www.mintic.gov.co/portal/inicio/Secciones-auxiliares/Politicas/2627:Politicas-de-Privacidad-y-Condiciones-de-Uso">política de privacidad</a> y el procesamiento de mis datos.
                        </label>
                        </div>

                    <div className="form-nav">
                        <button onClick={enviarFinal} className="btn btn-primary">Finalizar</button>
                    </div>
                </>
            )}
        </div>
        </motion.div>
    );
}