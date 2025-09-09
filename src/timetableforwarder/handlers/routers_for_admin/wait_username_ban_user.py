from logging import Logger, getLogger
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
import polib
from polib import POFile
from timetableforwarder.database.dao.banned_users_dao import BannedUsersDAO
from timetableforwarder.database.database_models import UserConfig, Admin, BannedUser
from timetableforwarder.database.dao.users_config_dao import UsersConfigDAO
from timetableforwarder.database.dao.admins_dao import AdminsDAO
from timetableforwarder.utils.get_config import GetConfig
from timetableforwarder.utils.del_user_searching_data import del_user_searching_data
from timetableforwarder.exceptions.users_exceptions import AttemptToBanAdminOrCreator


en_msgs: POFile = polib.pofile("locales/en/wait_username_ban_user.po")
ru_msgs: POFile = polib.pofile("locales/ru/wait_username_ban_user.po")

config: dict = GetConfig.get_bot_config()
creator_username: str = config["Settings"]["creator_username"]

action_logger: Logger = getLogger('action_logger')


async def get_username_for_ban_user_rout(message: Message, state: FSMContext) -> None:
    raw_input_username: str = message.text.strip()
    admin_username: str = message.from_user.username
    user_config: UserConfig = UsersConfigDAO().get_all_configs(username=admin_username)
    language: str = user_config.language

    finished_input_username: str = (
        raw_input_username
        if raw_input_username[0] != "@"
        else raw_input_username[1:]
    )

    match language:
        case "RU":
            msgs: POFile = ru_msgs
        case "EN":
            msgs: POFile = en_msgs
        case _:
            msgs: POFile = en_msgs
    admins: list[Admin] = AdminsDAO().get_admins()
    admins_usernames: list[str] = [admin.username for admin in admins]
    try:
        if (
            (admin_username in admins_usernames) or (finished_input_username == creator_username)
        ) and admin_username != creator_username:
            raise AttemptToBanAdminOrCreator(finished_input_username)

    except AttemptToBanAdminOrCreator:
        action_logger.critical(f"Admin $ @{admin_username} $ tried to block admin or creator $ @{finished_input_username} $")
        await message.answer(msgs.find("attempt_to_ban_admin_msg").msgstr)

    else:
        await del_user_searching_data(finished_input_username)
        if admin_username in admins_usernames:
            AdminsDAO().del_admin(username=finished_input_username)
            await message.answer(
                msgs.find("del_admin_msg").msgstr.format(
                    finished_input_username=finished_input_username
                )
            )

        banned_user: BannedUser = BannedUser(username=finished_input_username)
        BannedUsersDAO().ban_user(banned_user=banned_user)

        action_logger.warning(f"User $ @{finished_input_username} $ banned by admin $ {admin_username} $")
        await message.answer(
            msgs.find("user_banned_msg").msgstr.format(
                finished_input_username=finished_input_username
            )
        )

    finally:
        await state.clear()
