// app.js mejorado con Swal2 y UX pro

const LLM_API_URL = "https://llm-niza-classifier.onrender.com/predict_niza_classification";
const LLM_API_KEY = "TExNLU5pemEtQ2xhc3NpZmllci1CYWNrZW5k";
const BACKEND_API_URL = "https://llm-niza-classifier-backend.onrender.com/form_submission";
const BACKEND_API_KEY = "TExNLU5pemEtQ2xhc3NpZmllci1CYWNrZW5k";

async function clasificarYGuardar() {
    const datos = {
        nombre: document.getElementById("nombre").value,
        email: document.getElementById("email").value,
        edad: document.getElementById("edad").value,
        universidad: document.getElementById("universidad").value,
        carrera: document.getElementById("carrera").value,
        semestre: document.getElementById("semestre").value,
        experiencia_previa: document.getElementById("experiencia").value,
        nombre_emprendimiento: document.getElementById("nombre_emprendimiento").value,
        descripcion_emprendimiento: document.getElementById("descripcion").value,
        acepta_politica: document.getElementById("acepta").checked,
    };

    if (!datos.descripcion_emprendimiento || !datos.acepta_politica) {
        Swal.fire("Datos incompletos", "Debes aceptar la política y escribir una descripción válida.", "warning");
        return;
    }

    try {
        Swal.fire({
            title: "Clasificando...",
            text: "Analizando tu emprendimiento",
            allowOutsideClick: false,
            didOpen: () => Swal.showLoading()
        });

        const responseLLM = await fetch(LLM_API_URL, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "x-api-key": LLM_API_KEY,
            },
            body: JSON.stringify({ description: datos.descripcion_emprendimiento }),
        });

        const llmData = await responseLLM.json();
        datos.clasificaciones_niza = llmData.message.clasificaciones;

        const responseBackend = await fetch(BACKEND_API_URL, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "x-api-key": BACKEND_API_KEY,
            },
            body: JSON.stringify(datos),
        });

        const resultado = await responseBackend.json();
        Swal.close();

        Swal.fire("¡Éxito!", "Registro guardado correctamente.", "success");

        document.getElementById("resultado").innerHTML = `
            <h3>✔️ Registro exitoso</h3>
            <h4>Clasificaciones Niza sugeridas:</h4>
            <ul>
                ${datos.clasificaciones_niza.map(c => `
                <li style="margin-bottom:10px;">
                    <strong>Clase ${c.clase}</strong><br>
                    <em>${c.descripcion}</em><br>
                    Confianza: ${c.confianza}%<br>
                    Relevancia: ${c.relevancia || 'N/A'}
                </li>
                `).join('')}
            </ul>
            <a href="tablero.html">
                <button>Ver tablero</button>
            </a>
        `;

    } catch (error) {
        console.error("Error durante el envío:", error);
        Swal.fire("Error", "No se pudo completar el registro. Revisa la consola.", "error");
    }
}
