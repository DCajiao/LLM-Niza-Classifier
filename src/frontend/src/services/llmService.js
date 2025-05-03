// src/services/llmService.js
const LLM_API_URL = import.meta.env.VITE_LLM_API_URL;
const LLM_API_KEY = import.meta.env.VITE_LLM_API_KEY;

export async function obtenerClasificacionNiza(descripcion) {

    try {
        const response = await fetch(`${LLM_API_URL}/predict_niza_classification`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "x-api-key": LLM_API_KEY,
            },
            body: JSON.stringify({ description: descripcion }),
        });

        const data = await response.json();
        return data.message;
    } catch (error) {
        console.error("LLM error:", error);
        throw error;
    }
}
