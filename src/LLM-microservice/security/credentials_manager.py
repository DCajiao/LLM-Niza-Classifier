import os
from dotenv import load_dotenv


class CredentialsManager:
    @staticmethod
    def get_credentials():
        """
        Loads environment variables from a .env file and returns
        a dictionary.
        """
        load_dotenv()  # Load environment variables from .env file

        credentials = {
            "API_KEY": os.getenv("AI_STUDIO_API_KEY")
        }

        # Basic validation
        if not all(credentials.values()):
            raise ValueError(
                "Environment variables required for llm connection.")

        return credentials
