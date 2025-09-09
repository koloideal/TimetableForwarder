from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from timetableforwarder.database.database_models import UserConfig, Admin
from timetableforwarder.database.dao.users_config_dao import UsersConfigDAO
from timetableforwarder.utils.get_config import GetConfig
from timetableforwarder.database.dao.admins_dao import AdminsDAO
import polib
from polib import POFile


en_msgs: POFile = polib.pofile("locales/en/wait_username_add_admin.po")
ru_msgs: POFile = polib.pofile("locales/ru/wait_username_add_admin.po")


config: dict = GetConfig.get_bot_config()
creator_username: str = config["Settings"]["creator_username"]


async def get_username_for_add_admin_rout(message: Message, state: FSMContext) -> None:
    raw_input_username: str = message.text.strip()

    finished_input_username: str = (
        raw_input_username
        if raw_input_username[0] != "@"
        else raw_input_username[1:]
    )

    admin = Admin(username=finished_input_username)

    AdminsDAO().add_admin(admin=admin)
    user_config_dao: UsersConfigDAO = UsersConfigDAO()

    my_username: str = message.from_user.username
    my_config: UserConfig = user_config_dao.get_all_configs(username=my_username)
    language: str = my_config.language

    params: tuple = UserConfig.get_default_user_config(finished_input_username)
    user_config_dao.config_user_to_database(params=params)

    match language:
        case "RU":
            msgs: POFile = ru_msgs
        case "EN":
            msgs: POFile = en_msgs
        case _:
            msgs: POFile = en_msgs

    await message.answer(
        msgs.find("new_admin_msg").msgstr.format(
            finished_input_username=finished_input_username
        )
    )

    await state.clear()
