from logging import getLogger, Logger
from aiogram.types import Message
from aiogram.types import FSInputFile
from datetime import datetime
from aiogram.exceptions import TelegramBadRequest, TelegramNetworkError
from timetableforwarder.database.database_models import UserConfig
from timetableforwarder.database.dao.users_config_dao import UsersConfigDAO
import polib
from polib import POFile


en_msgs: POFile = polib.pofile("locales/en/get_logs_rout.po")
ru_msgs: POFile = polib.pofile("locales/ru/get_logs_rout.po")

action_logger: Logger = getLogger('action_logger')


async def get_logs_rout(message: Message) -> None:
    username: str = message.from_user.username
    command: str = message.text.strip()
    user_config: UserConfig = UsersConfigDAO().get_all_configs(username=username)
    language: str = user_config.language

    match language:
        case "RU":
            msgs: POFile = ru_msgs
        case "EN":
            msgs: POFile = en_msgs
        case _:
            msgs: POFile = en_msgs

    match command:
        case '/get_main_logs':
            file_name: str = "secret_data/main_logs.log"
        case '/get_action_logs':
            file_name: str = "secret_data/action_logs.log"
        case _:
            file_name: str = "secret_data/main_logs.log"
    document: FSInputFile = FSInputFile(file_name)
    captions: str = msgs.find("caption_msg").msgstr.format(date=datetime.now().strftime("%d-%m-%Y"))

    try:
        match command:
            case '/get_main_logs':
                action_logger.warning("Main bot logs have been successfully requested")
            case '/get_action_logs':
                action_logger.warning("Action bot logs have been successfully requested")
        await message.answer_document(document=document, caption=captions)

    except (TelegramBadRequest, TelegramNetworkError):
        match command:
            case '/get_main_logs':
                action_logger.warning("Main bot logs have been unsuccessfully requested")
            case '/get_action_logs':
                action_logger.warning("Action bot logs have been unsuccessfully requested")
        await message.answer(msgs.find("empty_logs_msg").msgstr)
