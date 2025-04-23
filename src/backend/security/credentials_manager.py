import os
from dotenv import load_dotenv


class CredentialsManager:
    @staticmethod
    def get_credentials():
        """
        Loads environment variables from a .env file and returns
        a dictionary with DB credentials.
        """
        load_dotenv()  # Load environment variables from .env file

        credentials = {
            "DB_HOST": os.getenv("DB_HOST"),
            "DB_PORT": int(os.getenv("DB_PORT", 5432)),  # default 5432
            "DB_USER": os.getenv("DB_USER"),
            "DB_PASSWORD": os.getenv("DB_PASSWORD"),
            "DB_NAME": os.getenv("DB_NAME")
        }

        # Basic validation
        if not all(credentials.values()):
            raise ValueError(
                "Faltan variables de entorno necesarias para la conexión a la base de datos.")

        return credentials
