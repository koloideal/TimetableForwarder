from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from polib import POFile
from findlybot.database.database_models import UserConfig, Admin
from findlybot.database.dao.users_config_dao import UsersConfigDAO
from findlybot.database.dao.admins_dao import AdminsDAO
import polib


en_msgs: POFile = polib.pofile("locales/en/wait_username_del_admin.po")
ru_msgs: POFile = polib.pofile("locales/ru/wait_username_del_admin.po")


async def get_username_for_del_admin_rout(message: Message, state: FSMContext) -> None:
    creator_username: str = message.from_user.username
    user_config: UserConfig = UsersConfigDAO().get_all_configs(username=creator_username)
    language: str = user_config.language

    match language:
        case "RU":
            msgs: POFile = ru_msgs
        case "EN":
            msgs: POFile = en_msgs
        case _:
            msgs: POFile = en_msgs
    try:
        admins: list[Admin] = AdminsDAO().get_admins()
        admin_usernames: list[str] = [admin.username for admin in admins]

        ex_admin_username: str = (
            message.text if message.text[0] != "@" else message.text[1:]
        )

        if ex_admin_username not in admin_usernames:
            raise TypeError

    except TypeError:
        await message.answer(msgs.find("not_admin_msg").msgstr)

    else:
        AdminsDAO().del_admin(username=ex_admin_username)

        await message.answer(
            msgs.find("admin_del_msg").msgstr.format(admin_username=ex_admin_username)
        )

    await state.clear()
