import tomllib
from dotenv import load_dotenv
import os


load_dotenv()


class GetConfig:
    @staticmethod
    def get_api_config() -> dict:
        with open("secret_data/config.toml", "rb") as config:
            config = tomllib.load(config)["API"]

        return config

    @staticmethod
    def get_bot_config() -> dict:
        with open("secret_data/config.toml", "rb") as config:
            config = tomllib.load(config)["Bot"]

        return config

    @staticmethod
    def get_database_config() -> dict:
        with open("secret_data/config.toml", "rb") as config:
            config = tomllib.load(config)["Database"]

        config['password'] = os.getenv('MYSQL_PASSWORD')

        return config
