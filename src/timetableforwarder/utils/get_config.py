from dataclasses import dataclass
import os
from dotenv import load_dotenv

load_dotenv()

@dataclass
class Config:
    bot_token: str
    database_url: str
    creator_id: int
    plpx_key: str

def load_config() -> Config:
    bot_token = os.environ["BOT_TOKEN"]

    plpx_key = os.environ["PLPX_API_KEY"]

    creator_id = int(os.environ["CREATOR_ID"])

    postgres_password = os.environ["POSTGRES_PASSWORD"]
    postgres_user = os.environ["POSTGRES_USER"]
    postgres_db = os.environ["POSTGRES_DB"]
    database_url = f"postgresql+psycopg://{postgres_user}:{postgres_password}@db:5432/{postgres_db}"

    return Config(
        bot_token=bot_token,
        database_url=database_url,
        plpx_key=plpx_key,
        creator_id=creator_id
    )
