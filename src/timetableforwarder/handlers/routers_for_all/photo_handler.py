from aiogram.types import Message
from timetableforwarder.utils.get_config import Config, load_config

config: Config = load_config()


async def handle_channel_photo(message: Message) -> None:
    if message.chat.id == config.channel_id and not message.caption:
        print("Photo from channel")
