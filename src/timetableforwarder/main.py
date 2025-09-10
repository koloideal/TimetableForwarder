from logging import Logger
import sys
from aiogram.client.session.aiohttp import AiohttpSession
from dishka import make_async_container
from dishka.integrations.aiogram import setup_dishka
from timetableforwarder.utils.set_commands import set_commands
from timetableforwarder.utils.make_dirs import make_dirs
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.client.bot import DefaultBotProperties
from aiogram.enums.parse_mode import ParseMode
from aiogram import Bot, Dispatcher
import asyncio

from timetableforwarder.di.providers import SQLAlchemyProvider, DAOProvider, ConfigProvider
from timetableforwarder.utils.get_config import Config, load_config
from timetableforwarder.handlers.main_routers import main_router
from timetableforwarder.handlers.group_router import group_router
from timetableforwarder.utils.create_loggers import create_main_logger, create_action_logger


config: Config = load_config()
bot_token: str = config.bot_token

session = AiohttpSession()
bot: Bot = Bot(token=bot_token, default=DefaultBotProperties(parse_mode=ParseMode.HTML), session=session)
storage: MemoryStorage = MemoryStorage()
dp: Dispatcher = Dispatcher(storage=storage)

main_logger: Logger = create_main_logger()
action_logger: Logger = create_action_logger()

container = make_async_container(SQLAlchemyProvider(), DAOProvider(), ConfigProvider())


async def main() -> None:
    make_dirs()

    main_logger.warning("Starting TimetableForwarder...")
    action_logger.critical("Starting logging actions...")
    dp.include_router(main_router)
    dp.include_router(group_router)
    
    setup_dishka(router=dp, container=container, auto_inject=True)
    await set_commands(bot, config)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

    print("\n\033[1m\033[30m\033[45m {} \033[0m".format("End of work..."))
    main_logger.warning("End of work...")
    action_logger.critical("End of logging actions...")
    exit()

if __name__ == "__main__":
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        
    print("\n\033[1m\033[30m\033[44m {} \033[0m".format("Starting TimetableForwarder..."))
    asyncio.run(main())
