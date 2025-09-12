from aiogram import Bot
from aiogram.exceptions import TelegramBadRequest, TelegramForbiddenError
from timetableforwarder.utils.get_config import Config


async def check_bot_rights(bot: Bot, config: Config) -> bool:
    me = await bot.me()
    try:
        await bot.get_chat_member(chat_id=config.channel_id, user_id=me.id)
    except (TelegramBadRequest, TelegramForbiddenError):
        return False
    else:
        return True
