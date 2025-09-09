import typing
from aiogram.types import FSInputFile, Message
import polib
from polib import POFile
from datetime import datetime
import json
import os

from timetableforwarder.database.database_models import UserConfig, Admin, SerializerDatabaseModels
from timetableforwarder.database.dao.users_config_dao import UsersConfigDAO
from timetableforwarder.database.dao.admins_dao import AdminsDAO

if typing.TYPE_CHECKING:
    from _typeshed import SupportsWrite


en_msgs: POFile = polib.pofile("locales/en/get_admins_rout.po")
ru_msgs: POFile = polib.pofile("locales/ru/get_admins_rout.po")


async def get_admins_rout(message: Message) -> None:
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

    all_admins: list[Admin] = AdminsDAO().get_admins()
    serialize_all_admins: dict[str, list] = SerializerDatabaseModels.admins_serialize(all_admins)

    if not all_admins:
        await message.answer(msgs.find("empty_database_msg").msgstr)
        return

    file_name: str = "secret_data/admin_users.json"

    with open(file_name, "w", encoding="utf8") as file:  # type: SupportsWrite[str]
        json.dump({'admins': serialize_all_admins}, file, indent=4, ensure_ascii=False)

    document: FSInputFile = FSInputFile(file_name)
    caption: str = msgs.find("caption_msg").msgstr.format(
        date=datetime.now().strftime("%d-%m-%Y")
    )
    await message.answer_document(document=document, caption=caption)
    os.remove(file_name)
