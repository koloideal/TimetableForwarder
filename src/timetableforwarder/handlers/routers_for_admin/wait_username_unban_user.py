from logging import Logger, getLogger
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from findlybot.database.database_models import BannedUser, UserConfig
from findlybot.database.dao.banned_users_dao import BannedUsersDAO
from findlybot.database.dao.users_config_dao import UsersConfigDAO
import polib
from polib import POFile


en_msgs: POFile = polib.pofile("locales/en/wait_username_unban_user.po")
ru_msgs: POFile = polib.pofile("locales/ru/wait_username_unban_user.po")

action_logger: Logger = getLogger('action_logger')


async def get_username_for_unban_user_rout(message: Message, state: FSMContext) -> None:
    admin_username: str = message.from_user.username
    user_config: UserConfig = UsersConfigDAO().get_all_configs(username=admin_username)
    lang: str = user_config.language

    match lang:
        case "RU":
            msgs: POFile = ru_msgs
        case "EN":
            msgs: POFile = en_msgs
        case _:
            msgs: POFile = en_msgs
    raw_input_username: str = message.text
    finished_input_username: str = (
        raw_input_username if raw_input_username[0] != "@" else raw_input_username[1:]
    )
    banned_users: list[BannedUser] = BannedUsersDAO().get_banned_users()
    banned_users_usernames: list[str] = [banned_user.username for banned_user in banned_users]
    is_banned: bool = finished_input_username in banned_users_usernames

    if is_banned:
        BannedUsersDAO().unban_user(username=finished_input_username)
        action_logger.warning(f"User $ @{finished_input_username} $ unbanned by admin $ @{admin_username} $")
        await message.answer(
            msgs.find("user_unban_msg").msgstr.format(
                finished_input_username=finished_input_username
            )
        )
    else:
        await message.answer(
            msgs.find("user_not_ban_msg").msgstr.format(
                finished_input_username=finished_input_username)
            )
    await state.clear()
