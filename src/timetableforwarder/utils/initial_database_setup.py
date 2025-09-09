from findlybot.database.dao.initialize_database_dao import InitializeDatabaseDAO
from findlybot.database.connect_to_database import DatabaseConnection
from findlybot.utils.get_config import GetConfig


config: dict = GetConfig.get_database_config()
host: str = config["host"]
user: int = config["user"]
password: str = config["password"]
database: str = config["database"]
port: int = config["port"]


def initial_database_setup() -> None:
    DatabaseConnection(host=host,
                       user=user,
                       password=password,
                       database=database,
                       port=port)
    InitializeDatabaseDAO().create_tables()

