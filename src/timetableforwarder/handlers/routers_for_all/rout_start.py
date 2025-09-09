from aiogram.types import Message
from findlybot.database.database_models import Admin, UserConfig, User
from findlybot.database.dao.users_dao import UsersDAO
from findlybot.database.dao.users_config_dao import UsersConfigDAO
from findlybot.database.dao.admins_dao import AdminsDAO
from findlybot.utils.get_config import GetConfig
import polib

en_msgs = polib.pofile("locales/en/rout_start.po")
ru_msgs = polib.pofile("locales/ru/rout_start.po")

config = GetConfig.get_bot_config()
creator_username: str = config["Settings"]["creator_username"]


async def start_rout(message: Message) -> None:
    users_config_dao: UsersConfigDAO = UsersConfigDAO()
    username: str = message.from_user.username
    user_id: int = message.from_user.id
    admins: list[Admin] = AdminsDAO().get_admins()
    admins_usernames: list[str] = [x.username for x in admins]

    user_config: UserConfig = users_config_dao.get_all_configs(username=username)
    lang: str = user_config.language

    match lang:
        case "RU":
            msgs = ru_msgs
        case "EN":
            msgs = en_msgs
        case _:
            msgs = en_msgs

    case1: bool = username in admins_usernames and username == creator_username
    case2: bool = username not in admins_usernames and username == creator_username
    case3: bool = username in admins_usernames and username != creator_username
    case4: bool = username not in admins_usernames and username != creator_username

    creator_case: bool = case1 or case2
    admin_case: bool = case3 and not (case1 or case2)
    user_case: bool = case4

    if creator_case:
        await message.answer(msgs.find("creator_case_msg").msgstr)

    elif admin_case:
        await message.answer(
            msgs.find("admin_case_msg").msgstr,
            disable_web_page_preview=True,
        )

    elif user_case:
        await message.answer(
            msgs.find("user_case_msg").msgstr,
            disable_web_page_preview=True,
        )

    username = message.from_user.username
    first_name = message.from_user.first_name

    UsersDAO().user_to_database(
        User(user_id=user_id,
             first_name=first_name,
             username=username)
    )
