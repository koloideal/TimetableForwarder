import polib
from aiogram import types

from timetableforwarder.database.database_models import UserConfig
from timetableforwarder.database.dao.users_config_dao import UsersConfigDAO


en_msgs = polib.pofile("locales/en/unknown_command.po")
ru_msgs = polib.pofile("locales/ru/unknown_command.po")


async def unknown_command(message: types.Message) -> None:
    username: str = message.from_user.username
    user_config: UserConfig = UsersConfigDAO().get_all_configs(username=username)
    language: str = user_config.language
    match language:
        case "RU":
            msgs = ru_msgs
        case "EN":
            msgs = en_msgs
        case _:
            msgs = en_msgs
    await message.answer(msgs.find("unknown_msg").msgstr)
