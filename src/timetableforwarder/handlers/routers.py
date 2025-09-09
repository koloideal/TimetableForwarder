from aiogram import Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
from dishka.integrations.aiogram import FromDishka

from timetableforwarder.database.dao.users_dao import UsersDAO
from timetableforwarder.handlers.routers_for_admin.wait_username_ban_user import get_username_for_ban_user_rout
from timetableforwarder.handlers.routers_for_admin.wait_username_unban_user import get_username_for_unban_user_rout
from timetableforwarder.handlers.routers_for_all.rout_help import help_rout
from timetableforwarder.handlers.routers_for_all.rout_start import start_rout
from timetableforwarder.handlers.routers_for_admin.ban_or_unban_user_rout import ban_or_unban_user_rout
from timetableforwarder.handlers.routers_for_all.unknown_command import unknown_command
from timetableforwarder.middlewares.is_user_blocked import RejectBlockedUserMiddleware
from timetableforwarder.middlewares.is_user_creator import RejectNotCreatorMiddleware
from timetableforwarder.states.admin_states import AdminState


router: Router = Router()
router.message.middleware(RejectBlockedUserMiddleware())
router.message.middleware(RejectNotCreatorMiddleware())


@router.message(Command("start"))
async def start_routing(message: Message, users_dao: FromDishka[UsersDAO]) -> None:
    await start_rout(message, users_dao)

@router.message(Command("help"))
async def help_routing(message: Message) -> None:
    await help_rout(message)

@router.message(Command("ban_user"))
async def ban_user_routing(message: Message, state: FSMContext) -> None:
    await ban_or_unban_user_rout(message, "ban", state)

@router.message(Command("unban_user"))
async def unban_user_routing(message: Message, state: FSMContext) -> None:
    await ban_or_unban_user_rout(message, "unban", state)

@router.message(AdminState.waiting_for_ban_user)
async def get_username_for_ban_user(message: Message, state: FSMContext, users_dao: FromDishka[UsersDAO]) -> None:
    await get_username_for_ban_user_rout(message, state)


@router.message(AdminState.waiting_for_unban_user)
async def get_username_for_unban_user(message: Message, state: FSMContext, users_dao: FromDishka[UsersDAO]) -> None:
    await get_username_for_unban_user_rout(message, state)

@router.message()
async def unknown_command_routing(message: Message) -> None:
    await unknown_command(message)
