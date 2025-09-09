from aiogram import types
from findlybot.database.database_models import UserConfig
from findlybot.database.dao.users_config_dao import UsersConfigDAO
from findlybot.states.admin_states import AdminState
from aiogram.fsm.context import FSMContext
import polib
from polib import POFile


en_msgs: POFile = polib.pofile("locales/en/ban_or_unban_user_rout.po")
ru_msgs: POFile = polib.pofile("locales/ru/ban_or_unban_user_rout.po")


async def ban_or_unban_user_rout(
    message: types.Message, ban_or_unban: str, state: FSMContext
) -> None:
    username: str = message.from_user.username
    user_config: UserConfig = UsersConfigDAO().get_all_configs(username=username)
    language: str = user_config.language

    match language:
        case "RU":
            msgs: POFile = ru_msgs
        case "EN":
            msgs: POFile = en_msgs
        case _:
            msgs: POFile = en_msgs

    await message.answer(msgs.find("enter_username_msg").msgstr)

    match ban_or_unban:
        case "ban":
            await state.set_state(AdminState.waiting_for_ban_user)
        case "unban":
            await state.set_state(AdminState.waiting_for_unban_user)
