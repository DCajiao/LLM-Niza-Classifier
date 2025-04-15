import json
import os

# Importar la función de Hugging Face
from llm_huggingface import obtener_clasificaciones_niza_hf

# Función para obtener una clasificación de ejemplo (para desarrollo/testing)
def obtener_clasificacion_ejemplo():
    """
    Devuelve una clasificación Niza de ejemplo para propósitos de desarrollo
    cuando no se puede acceder a la API de OpenAI.
    
    Returns:
        dict: Clasificación Niza de ejemplo
    """
    return {
        "clasificaciones": [
            {
                "clase": "42",
                "descripcion": "Servicios científicos y tecnológicos, así como servicios de investigación y diseño conexos; servicios de análisis industrial, investigación industrial y diseño industrial; control de calidad y servicios de autenticación; diseño y desarrollo de hardware y software.",
                "relevancia": "Esta clasificación es relevante para el desarrollo de aplicaciones tecnológicas y servicios de diseño de software.",
                "confianza": "95"
            },
            {
                "clase": "41",
                "descripcion": "Educación; formación; servicios de entretenimiento; actividades deportivas y culturales.",
                "relevancia": "Aplicable para los componentes educativos y de formación de la plataforma.",
                "confianza": "85"
            },
            {
                "clase": "35",
                "descripcion": "Publicidad; gestión, organización y administración de negocios comerciales; trabajos de oficina.",
                "relevancia": "Relevante para los aspectos de administración y gestión empresarial del proyecto.",
                "confianza": "75"
            }
        ]
    }
