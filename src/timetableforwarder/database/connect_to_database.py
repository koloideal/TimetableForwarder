import mysql.connector
from mysql.connector.abstracts import MySQLCursorAbstract
from mysql.connector.errors import DatabaseError
from mysql.connector.errors import ProgrammingError
from logging import getLogger, Logger
from typing import TypeVar, Generic


main_logger: Logger = getLogger('root')
DatabaseConnectionType = TypeVar('DatabaseConnectionType')


class DatabaseConnection(Generic[DatabaseConnectionType]):
    _kwargs: dict[str, str] | None = None
    _instance: DatabaseConnectionType | None = None

    def __new__(cls, **kwargs):
        if cls._instance is None:
            cls._kwargs = kwargs
            try:
                mysql.connector.connect(**DatabaseConnection._kwargs)
            except ProgrammingError as e:
                main_logger.error(f"Error connecting to database: {e}")
                raise
            except DatabaseError as e:
                main_logger.error(f"Error connecting to database: {e}")
                raise
            else:
                cls._instance = super(DatabaseConnection, cls).__new__(cls)

        return cls._instance

    def __enter__(self) -> MySQLCursorAbstract:
        self.connection = mysql.connector.connect(**DatabaseConnection._kwargs)
        self.cursor = self.connection.cursor()
        return self.cursor

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.connection.commit()
        self.connection.close()

    @classmethod
    def __del__(cls):
        if cls._instance:
            main_logger.critical("delete db singleton instance")
            cls._instance = None
            cls._kwargs = None

