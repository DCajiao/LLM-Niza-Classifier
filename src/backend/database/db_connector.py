import sqlalchemy
from sqlalchemy.pool import QueuePool
import logging
import pandas as pd

from security.credentials_manager import CredentialsManager

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DatabaseManager:
    def __init__(self, pool_size=5, max_overflow=2):
        """
        Initializes the database manager with connection pooling.

        :param pool_size: Number of connections in the pool.
        :param max_overflow: Max overflow connections.
        """
        self.credentials = CredentialsManager.get_credentials()

        # Configuration of the connection pool with SQLAlchemy
        self.pool = self._create_pool(pool_size, max_overflow)

    def _create_pool(self, pool_size, max_overflow):
        """
        Creates a connection pool using SQLAlchemy.
        """
        try:
            db_host = self.credentials["DB_HOST"]
            db_port = self.credentials.get("DB_PORT", 5432)
            db_user = self.credentials["DB_USER"]
            db_password = self.credentials["DB_PASSWORD"]
            db_name = self.credentials["DB_NAME"]

            connection_url = sqlalchemy.engine.URL.create(
                drivername="postgresql+pg8000",
                username=db_user,
                password=db_password,
                host=db_host,
                port=db_port,
                database=db_name,
            )

            engine = sqlalchemy.create_engine(
                connection_url,
                poolclass=QueuePool,
                pool_size=pool_size,
                max_overflow=max_overflow,
                pool_timeout=30,
                pool_recycle=1800
            )
            return engine
        except Exception as e:
            logger.error(f"Error creating connection pool: {e}")
            raise e

    def execute_query(self, query, params=None, fetch=False):
        """
        Executes a SQL query using the connection pool.
        """
        try:
            with self.pool.connect() as connection:
                with connection.begin():
                    result = connection.execute(sqlalchemy.text(query), params or {})

                    if fetch:
                        rows = result.fetchall()
                        return pd.DataFrame(rows, columns=result.keys()) if rows else pd.DataFrame()
        except Exception as e:
            logger.error(f"Error executing query: {e}")
            raise e

    def close_pool(self):
        """
        Closes the connection pool.
        """
        try:
            if self.pool:
                self.pool.dispose()
            logger.info("Database connection pool closed successfully.")
        except Exception as e:
            logger.error(f"Error closing the connection pool: {e}")
            raise e
