from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
from aiogram.enums.chat_type import ChatType
from dishka.integrations.aiogram import FromDishka

from timetableforwarder.database.dao.users_dao import UsersDAO
from timetableforwarder.handlers.routers_for_admin.get_list_of_banned import get_list_of_banned
from timetableforwarder.handlers.routers_for_admin.get_list_of_all_users import get_list_of_all_users
from timetableforwarder.handlers.routers_for_admin.wait_username_ban_user import get_username_for_ban_user_rout
from timetableforwarder.handlers.routers_for_admin.wait_username_unban_user import get_username_for_unban_user_rout
from timetableforwarder.handlers.routers_for_all.rout_help import help_rout
from timetableforwarder.handlers.routers_for_all.rout_start import start_rout
from timetableforwarder.handlers.routers_for_admin.ban_or_unban_user_rout import ban_or_unban_user_rout
from timetableforwarder.handlers.routers_for_all.unknown_command import unknown_command
from timetableforwarder.handlers.routers_for_all.subscriptions import open_config, select_group, select_off, go_back
from timetableforwarder.handlers.routers_for_all.photo_handler import handle_channel_photo
from timetableforwarder.database.dao.subscribed_groups_dao import SubscribedGroupsDAO
from timetableforwarder.handlers.routers_for_admin.del_group_flow import del_group_entry, del_group_select, del_group_yes, del_group_no, del_group_back
from timetableforwarder.handlers.routers_for_admin.mailing_flow import mailing_cmd, mailing_receive, mailing_send, mailing_cancel
from timetableforwarder.handlers.routers_for_admin.add_group_flow import add_group_cmd, add_group_receive
from timetableforwarder.middlewares.is_user_blocked import RejectBlockedUserMiddleware
from timetableforwarder.middlewares.is_user_creator import RejectNotCreatorMiddleware
from timetableforwarder.states.admin_states import AdminState
from timetableforwarder.utils.get_config import load_config, Config


main_router: Router = Router()
main_router.message.filter(F.chat.type.in_({ChatType.SENDER, ChatType.PRIVATE}))
main_router.message.middleware(RejectBlockedUserMiddleware())
main_router.message.middleware(RejectNotCreatorMiddleware())


@main_router.message(Command("start"))
async def start_routing(message: Message, users_dao: FromDishka[UsersDAO]) -> None:
    await start_rout(message, users_dao)

@main_router.message(Command("help"))
async def help_routing(message: Message) -> None:
    await help_rout(message)

@main_router.message(Command("del_group"))
async def del_group_cmd(message: Message) -> None:
    await del_group_entry(message)

@main_router.message(Command("add_group"))
async def add_group_command(message: Message, state: FSMContext) -> None:
    await add_group_cmd(message, state)

@main_router.message(Command("mailing"))
async def mailing_command(message: Message, state: FSMContext) -> None:
    await mailing_cmd(message, state)

@main_router.message(Command("ban_user"))
async def ban_user_routing(message: Message, state: FSMContext) -> None:
    await ban_or_unban_user_rout(message, "ban", state)

@main_router.message(Command("unban_user"))
async def unban_user_routing(message: Message, state: FSMContext) -> None:
    await ban_or_unban_user_rout(message, "unban", state)

@main_router.message(AdminState.waiting_for_ban_user)
async def get_username_for_ban_user(message: Message, state: FSMContext, users_dao: FromDishka[UsersDAO]) -> None:
    await get_username_for_ban_user_rout(message, state, users_dao)

@main_router.message(AdminState.waiting_for_unban_user)
async def get_username_for_unban_user(message: Message, state: FSMContext, users_dao: FromDishka[UsersDAO]) -> None:
    await get_username_for_unban_user_rout(message, state, users_dao)

@main_router.message(Command("list_banned"))
async def get_list_of_banned_routing(message: Message, users_dao: FromDishka[UsersDAO]) -> None:
    await get_list_of_banned(message, users_dao)

@main_router.message(Command("list_all_users"))
async def get_list_of_all_users_routing(message: Message, users_dao: FromDishka[UsersDAO]) -> None:
    await get_list_of_all_users(message, users_dao)

@main_router.callback_query(F.data == "cfg_open")
async def cfg_open_routing(cb: CallbackQuery, users_dao: FromDishka[UsersDAO]) -> None:
    await open_config(cb, users_dao)

@main_router.callback_query(F.data.startswith("cfg_group:"))
async def cfg_group_routing(cb: CallbackQuery, users_dao: FromDishka[UsersDAO]) -> None:
    group = int(cb.data.split(":", 1)[1])
    await select_group(cb, users_dao, group)

@main_router.callback_query(F.data == "cfg_off")
async def cfg_off_routing(cb: CallbackQuery, users_dao: FromDishka[UsersDAO]) -> None:
    await select_off(cb, users_dao)

@main_router.callback_query(F.data == "cfg_back")
async def cfg_back_routing(cb: CallbackQuery, users_dao: FromDishka[UsersDAO]) -> None:
    await go_back(cb, users_dao)

@main_router.callback_query(F.data == "del_open")
async def del_open_routing(cb: CallbackQuery) -> None:
    await del_group_entry(cb.message)
    await cb.answer()

@main_router.callback_query(F.data.startswith("del_grp:"))
async def del_select_routing(cb: CallbackQuery) -> None:
    group = int(cb.data.split(":", 1)[1])
    await del_group_select(cb, group)

@main_router.callback_query(F.data.startswith("del_yes:"))
async def del_yes_routing(cb: CallbackQuery, users_dao: FromDishka[UsersDAO]) -> None:
    group = int(cb.data.split(":", 1)[1])
    await del_group_yes(cb, group, users_dao)

@main_router.callback_query(F.data == "del_no")
async def del_no_routing(cb: CallbackQuery) -> None:
    await del_group_no(cb)

@main_router.callback_query(F.data == "del_return")
async def del_return_routing(cb: CallbackQuery, users_dao: FromDishka[UsersDAO]) -> None:
    await del_group_back(cb, users_dao)

@main_router.channel_post(F.chat.id == load_config().channel_id, F.photo, ~F.media_group_id)
async def photo_routing(
    message: Message,
    users_dao: FromDishka[UsersDAO],
    subscribed_groups_dao: FromDishka[SubscribedGroupsDAO],
    config: FromDishka[Config],
) -> None:
    await handle_channel_photo(message, config, users_dao, subscribed_groups_dao)

@main_router.message(AdminState.waiting_for_mailing)
async def mailing_receive_routing(message: Message, state: FSMContext) -> None:
    await mailing_receive(message, state)

@main_router.callback_query(F.data == "mail_yes")
async def mailing_yes_routing(cb: CallbackQuery, state: FSMContext, users_dao: FromDishka[UsersDAO], config: FromDishka[Config]) -> None:
    await mailing_send(cb, state, users_dao, config)

@main_router.callback_query(F.data == "mail_no")
async def mailing_no_routing(cb: CallbackQuery, state: FSMContext, users_dao: FromDishka[UsersDAO]) -> None:
    await mailing_cancel(cb, state, users_dao)
    
@main_router.message(AdminState.waiting_for_add_group)
async def add_group_receive_routing(message: Message, state: FSMContext) -> None:
    await add_group_receive(message, state)

@main_router.message()
async def unknown_command_routing(message: Message) -> None:
    await unknown_command(message)
