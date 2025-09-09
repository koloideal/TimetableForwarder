from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, Message
from timetableforwarder.database.database_models import UserConfig
from timetableforwarder.database.dao.users_config_dao import UsersConfigDAO
import polib
from timetableforwarder.utils.get_config import GetConfig


config: dict = GetConfig.get_bot_config()
en_msgs = polib.pofile("locales/en/is_user_creator.po")
ru_msgs = polib.pofile("locales/ru/is_user_creator.po")
creator_username: str = config["Settings"]["creator_username"]


class RejectNotCreatorMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: Message,
            data: Dict[str, Any]
    ) -> Any:
        if not event.text:
            return
        username: str = event.from_user.username
        user_config: UserConfig = UsersConfigDAO().get_all_configs(username=username)
        language: str = user_config.language

        match language:
            case "RU":
                msgs = ru_msgs
            case "EN":
                msgs = en_msgs
            case _:
                msgs = en_msgs
        creator_commands = ['/add_admin', '/del_admin', 'drop_data', '/get_admins']
        if event.text.strip() in creator_commands:
            if username == creator_username:
                return await handler(event, data)
            else:
                await event.answer(msgs.find("unknown_command_msg").msgstr)
        else:
            return await handler(event, data)