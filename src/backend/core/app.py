import logging
import json

from datetime import datetime

from database.db_connector import DatabaseManager

############# CONFIGURATION #############
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

db_connector = DatabaseManager()
#########################################


def insert_data(form_data: dict):
    try:
        logging.info("Inserting data into the database")

        # Validate the form data
        if not form_data_validation(form_data):
            logging.error("Form data validation failed")
            raise ValueError("Invalid form data")

        # Read the SQL query from the file
        with open("sql/insert_emprendedores.sql", "r") as file:
            query = file.read()

        # Prepare the data for insertion
        form_data["clasificaciones_niza"] = json.dumps(
            form_data["clasificaciones_niza"])

        # If the 'edad' field is empty, set it to 0
        if not form_data["edad"]:
            form_data["edad"] = 0

        db_connector.execute_query(query, form_data)
        logging.info("Data inserted successfully")
        return {
            "status": "success",
            "message": "Data inserted successfully"
        }

    except Exception as e:
        logging.error(f"Error inserting data: {e}")
        return {
            "status": "error",
            "message": str(e)
        }


def form_data_validation(form_data: dict) -> bool:
    # Check if all required fields are present
    required_fields = [
        #"nombre",
        #"email",
        #"edad",
        "universidad",
        "carrera",
        "semestre",
        "experiencia_previa",
        "nombre_emprendimiento",
        "descripcion_emprendimiento",
        "clasificaciones_niza",
        "acepta_politica"
    ]

    for field in required_fields:
        if field not in form_data or not form_data[field]:
            return False

    return True
