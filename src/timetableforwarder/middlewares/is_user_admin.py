from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, Message
from findlybot.database.dao.admins_dao import AdminsDAO
from findlybot.database.database_models import Admin, UserConfig
from findlybot.database.dao.users_config_dao import UsersConfigDAO
import polib
from findlybot.utils.get_config import GetConfig


config: dict = GetConfig.get_bot_config()
en_msgs = polib.pofile("locales/en/is_user_admin.po")
ru_msgs = polib.pofile("locales/ru/is_user_admin.po")
creator_username: str = config["Settings"]["creator_username"]


class RejectNotAdminMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: Message,
            data: Dict[str, Any]
    ) -> Any:
        if not event.text:
            return
        admins: list[Admin] = AdminsDAO().get_admins()
        admins_usernames: list[str] = [x.username for x in admins]
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
        admin_commands = ['/ban_user', '/unban_user', '/get_main_logs', '/get_action_logs']
        if event.text.strip() in admin_commands:
            if username in admins_usernames or username == creator_username:
                return await handler(event, data)
            else:
                await event.answer(msgs.find("unknown_command_msg").msgstr)
        else:
            return await handler(event, data)