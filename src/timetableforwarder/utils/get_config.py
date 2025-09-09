from dataclasses import dataclass
import tomli
from pathlib import Path

@dataclass
class Config:
    bot_token: str
    database_url: str
    creator_id: int
    channel_id: int
    plpx_key: str
    groups: list[int]

def load_config() -> Config:
    config_path = Path("secret_data/config.toml")
    
    with open(config_path, "rb") as f:
        config_data = tomli.load(f)
    
    bot_config = config_data["bot"]
    db_config = config_data["database"]
    external_config = config_data["external"]
    groups_config = config_data["groups"]
    
    database_url = f"postgresql+asyncpg://{db_config['postgres_user']}:{db_config['postgres_password']}@localhost:5432/{db_config['postgres_db']}"
    
    return Config(
        bot_token=bot_config["token"],
        database_url=database_url,
        plpx_key=external_config["pplx_api_key"],
        creator_id=bot_config["creator_id"],
        channel_id=bot_config["channel_id"],
        groups=groups_config["list"]
    )
