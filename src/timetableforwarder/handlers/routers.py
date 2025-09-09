from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
from timetableforwarder.handlers.routers_for_all.rout_config import config_rout
from timetableforwarder.handlers.routers_for_all.rout_help import button_to_help_rout
from timetableforwarder.handlers.routers_for_all.rout_start import start_rout
from timetableforwarder.handlers.routers_for_admin.add_or_del_admin_rout import add_or_del_admin_rout
from timetableforwarder.handlers.routers_for_admin.ban_or_unban_user_rout import ban_or_unban_user_rout
from timetableforwarder.handlers.routers_for_admin.wait_username_add_admin import get_username_for_add_admin_rout
from timetableforwarder.handlers.routers_for_admin.wait_username_del_admin import get_username_for_del_admin_rout
from timetableforwarder.handlers.routers_for_admin.wait_username_ban_user import get_username_for_ban_user_rout
from timetableforwarder.handlers.routers_for_admin.wait_username_unban_user import get_username_for_unban_user_rout
from timetableforwarder.handlers.routers_for_admin.get_logs_rout import get_logs_rout
from timetableforwarder.handlers.routers_for_admin.get_admins_rout import get_admins_rout
from timetableforwarder.handlers.routers_for_admin.drop_data import drop_data_rout
from timetableforwarder.states.admin_states import AdminState
from timetableforwarder.states.user_states import WaitQuery, WaitMaxSize
from timetableforwarder.handlers.routers_for_all.rout_search import search_rout
from timetableforwarder.handlers.routers_for_all.unknown_command import unknown_command
from timetableforwarder.handlers.routers_for_all.wait_query_to_search import get_query_to_search_rout
from timetableforwarder.handlers.routers_for_all.wait_max_size import get_max_size_rout
from .callback_query import (
    callback_query_swipe_items,
    callback_query_change_config,
    callback_query_max_size
)
from timetableforwarder.handlers.custom_callback_data.swipe_items_callback_data import SwipeItemsCallbackData
from timetableforwarder.middlewares.is_user_blocked import RejectBlockedUserMiddleware
from timetableforwarder.middlewares.is_user_admin import RejectNotAdminMiddleware
from timetableforwarder.middlewares.is_user_creator import RejectNotCreatorMiddleware


router: Router = Router()
router.message.middleware(RejectBlockedUserMiddleware())
router.message.middleware(RejectNotAdminMiddleware())
router.message.middleware(RejectNotCreatorMiddleware())


@router.message(Command("start"))
async def start_routing(message: Message) -> None:
    await start_rout(message)


@router.message(Command("help"))
async def help_routing(message: Message) -> None:
    await button_to_help_rout(message)


@router.message(Command("add_admin"))
async def add_admin_routing(message: Message, state: FSMContext) -> None:
    await add_or_del_admin_rout(message, "add", state)


@router.message(Command("del_admin"))
async def del_admin_routing(message: Message, state: FSMContext) -> None:
    await add_or_del_admin_rout(message, "del", state)


@router.message(Command("ban_user"))
async def ban_user_routing(message: Message, state: FSMContext) -> None:
    await ban_or_unban_user_rout(message, "ban", state)


@router.message(Command("unban_user"))
async def unban_user_routing(message: Message, state: FSMContext) -> None:
    await ban_or_unban_user_rout(message, "unban", state)


@router.message(Command("get_main_logs"))
async def get_main_logs_routing(message: Message) -> None:
    await get_logs_rout(message)


@router.message(Command("get_action_logs"))
async def get_action_logs_routing(message: Message) -> None:
    await get_logs_rout(message)


@router.message(Command("get_admins"))
async def get_admin_bd_routing(message: Message) -> None:
    await get_admins_rout(message)


@router.message(Command("search"))
async def search_routing(message: Message, state: FSMContext) -> None:
    await search_rout(message, state)


@router.message(Command("config"))
async def config_routing(message: Message) -> None:
    await config_rout(message)


@router.message(F.text == "drop data")
async def drop_data_routing(message: Message) -> None:
    await drop_data_rout(message)


@router.message(AdminState.waiting_for_add_admin)
async def get_username_for_add_admin(message: Message, state: FSMContext) -> None:
    await get_username_for_add_admin_rout(message, state)


@router.message(AdminState.waiting_for_del_admin)
async def get_username_for_del_admin(message: Message, state: FSMContext) -> None:
    await get_username_for_del_admin_rout(message, state)


@router.message(AdminState.waiting_for_ban_user)
async def get_username_for_ban_user(message: Message, state: FSMContext) -> None:
    await get_username_for_ban_user_rout(message, state)


@router.message(AdminState.waiting_for_unban_user)
async def get_username_for_unban_user(message: Message, state: FSMContext) -> None:
    await get_username_for_unban_user_rout(message, state)


@router.message(WaitQuery.wait_query)
async def get_query_to_search(message: Message, state: FSMContext) -> None:
    await get_query_to_search_rout(message, state)


@router.message(WaitMaxSize.wait_max_size)
async def get_max_size(message: Message, state: FSMContext) -> None:
    await get_max_size_rout(message, state)


@router.callback_query(SwipeItemsCallbackData.filter())
async def swipe_items(callback_query: CallbackQuery,
                      callback_data: SwipeItemsCallbackData) -> None:
    await callback_query_swipe_items(callback_query, callback_data)


@router.callback_query(F.data[-2:].in_(['ON', 'FF', 'EN', 'RU']))
async def change_config(callback_query: CallbackQuery) -> None:
    await callback_query_change_config(callback_query)


@router.callback_query(F.data == "change_max_size")
async def change_max_size(callback_query: CallbackQuery, state: FSMContext) -> None:
    await callback_query_max_size(callback_query, state)


@router.message()
async def unknown_command_routing(message: Message) -> None:
    await unknown_command(message)
