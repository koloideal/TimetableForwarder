from aiogram import types
from findlybot.database.database_models import UserConfig
from findlybot.states.admin_states import AdminState
from aiogram.fsm.context import FSMContext
from findlybot.database.dao.users_config_dao import UsersConfigDAO
import polib
from polib import POFile


en_msgs: POFile = polib.pofile("locales/en/add_or_del_admin_rout.po")
ru_msgs: POFile = polib.pofile("locales/ru/add_or_del_admin_rout.po")


async def add_or_del_admin_rout(
    message: types.Message, del_or_add: str, state: FSMContext
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
    match del_or_add:
        case "add":
            await state.set_state(AdminState.waiting_for_add_admin)
        case "del":
            await state.set_state(AdminState.waiting_for_del_admin)
