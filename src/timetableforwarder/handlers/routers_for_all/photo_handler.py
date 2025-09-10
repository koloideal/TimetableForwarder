from aiogram.types import Message
from timetableforwarder.utils.get_config import Config, load_config

config: Config = load_config()


async def handle_channel_photo(message: Message) -> None:
    if message.caption:
        return
    
    await message.answer("🎓 <b>Расписание</b>\n\n"
                         "🔍 <b>Расписание</b>\n\n"
                         "🔍 <b>Расписание</b>\n\n")
