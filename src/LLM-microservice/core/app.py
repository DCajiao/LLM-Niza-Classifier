import json
import logging

from google import genai

import utils.definitions as definitions
from security.credentials_manager import CredentialsManager

############# CONFIGURATION #############
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

API_KEY = CredentialsManager.get_credentials()['API_KEY']
#########################################


def build_prompt(description):
    """
    Construye un prompt para el modelo Gemini basado en la descripción del emprendimiento.

    Args:
        description (str): Descripción detallada del emprendimiento.

    Returns:
        str: Prompt construido para el modelo.
    """
    prompt = f"""Analiza la siguiente descripción de un emprendimiento y determina las 3 clasificaciones Niza más relevantes.

    Descripción del emprendimiento:
    {description}

    Las clasificaciones Niza son:
    {json.dumps(str(definitions.NIZA_CLASSIFICATIONS), indent=2)}

    Devuelve solo un JSON con el siguiente formato exacto sin incluir texto adicional, ni saltos de línea:
    {{
    "clasificaciones": [
        {{
        "clase": "NÚMERO_DE_CLASE",
        "descripcion": "DESCRIPCIÓN_OFICIAL_DE_LA_CLASE",
        "relevancia": "EXPLICACIÓN_DE_POR_QUÉ_ES_RELEVANTE",
        "confianza": PORCENTAJE_DE_CONFIANZA_ENTRE_0_Y_100
        }},
        ...
    ]
    }}"""

    return prompt


def get_classification_niza(description):
    """
    Analiza la descripción del emprendimiento utilizando Gemini para determinar
    las clasificaciones Niza más apropiadas.

    Args:
        descripcion (str): Descripción detallada del emprendimiento.

    Returns:
        dict: Diccionario con las clasificaciones Niza relevantes.
    """
    try:
        # Build the prompt
        prompt = build_prompt(description)

        # Connect to the Gemini model
        client = genai.Client(api_key=API_KEY)
        response = client.models.generate_content(
            model="gemini-1.5-flash",
            contents=prompt
        )

        generated_text = response.text.strip()
        generated_text = generated_text.encode('utf-8').decode('utf-8')
        
        
        

        # Search for the JSON within the response
        start = generated_text.find("{")
        end = generated_text.rfind("}") + 1
        json_string = generated_text[start:end]

        result = json.loads(json_string)
        #print(f"Respuesta del modelo: {json_string}")

        # Check if the JSON is valid
        if "clasificaciones" in result:
            for item in result["clasificaciones"]:
                item["confianza"] = int(item.get("confianza", 0))
            return result

        else:
            print(f"Respuesta inesperada del modelo: {generated_text}")
            raise ValueError("Formato inválido en la respuesta del modelo")

    except Exception as e:
        print(f"Error: {e}")
        return {
            "clasificaciones": [
                {
                    "clase": "Error",
                    "descripcion": str(e),
                    "relevancia": "No se pudo procesar correctamente la respuesta del modelo.",
                    "confianza": 0
                }
            ]
        }
