from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from timetableforwarder.database.database_models import UserConfig
from timetableforwarder.database.dao.users_config_dao import UsersConfigDAO
from html import escape
import polib

en_msgs = polib.pofile("locales/en/wait_max_size.po")
ru_msgs = polib.pofile("locales/ru/wait_max_size.po")


async def get_max_size_rout(message: Message, state: FSMContext) -> None:
    username = message.from_user.username
    user_config: UserConfig = UsersConfigDAO().get_all_configs(username=username)
    language: str = user_config.language

    match language:
        case "RU":
            msgs = ru_msgs
        case "EN":
            msgs = en_msgs
        case _:
            msgs = en_msgs
    try:
        max_size: int = int(message.text.strip())
        if not 0 < max_size <= 40:
            raise ValueError
    except ValueError:
        text: str = escape("0 < max_size <= 40")
        await message.answer(msgs.find("incorrect_value_msg").msgstr.format(text=text))
    else:
        UsersConfigDAO().change_max_size_config(username=username, max_size=max_size)
        await message.answer(
            msgs.find("change_max_size_msg").msgstr.format(max_size=max_size)
        )
        await state.clear()
