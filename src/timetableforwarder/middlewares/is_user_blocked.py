from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, Message
from timetableforwarder.database.database_models import UserConfig, BannedUser
from timetableforwarder.database.dao.users_config_dao import UsersConfigDAO
from timetableforwarder.database.dao.banned_users_dao import BannedUsersDAO
import polib


en_msgs = polib.pofile("locales/en/is_user_blocked.po")
ru_msgs = polib.pofile("locales/ru/is_user_blocked.po")


class RejectBlockedUserMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: Message,
            data: Dict[str, Any]
    ) -> Any:
        if not event.text:
            return
        banned_users: list[BannedUser] = BannedUsersDAO().get_banned_users()
        banned_users_usernames: list[str] = [banned_user.username for banned_user in banned_users]
        username: str = event.from_user.username

        params: tuple = UserConfig.get_default_user_config(username=username)
        UsersConfigDAO().config_user_to_database(params=params)

        user_config: UserConfig = UsersConfigDAO().get_all_configs(username=username)
        language: str = user_config.language

        match language:
            case "RU":
                msgs = ru_msgs
            case "EN":
                msgs = en_msgs
            case _:
                msgs = en_msgs

        if username in banned_users_usernames:
            await event.answer(
                msgs.find("banned_user_case_msg").msgstr,
                disable_web_page_preview=True,
            )
        else:
            return await handler(event, data)