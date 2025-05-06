const BACKEND_API_URL = import.meta.env.VITE_BACKEND_API_URL;
const BACKEND_API_KEY = import.meta.env.VITE_BACKEND_API_KEY;

export async function guardarRegistro(data) {
  try {
    const response = await fetch(`${BACKEND_API_URL}/form_submission`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "x-api-key": BACKEND_API_KEY,
      },
      body: JSON.stringify(data),
    });

    if (!response.ok) throw new Error("Error al guardar los datos");

    const resultado = await response.json();
    return resultado;
  } catch (error) {
    console.error("Error al guardar:", error);
    throw error;
  }
}
