from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton, InputMediaPhoto
from aiogram.fsm.context import FSMContext
from aiogram.exceptions import TelegramBadRequest, TelegramForbiddenError
from timetableforwarder.states.admin_states import AdminState
from timetableforwarder.database.dao.users_dao import UsersDAO
from timetableforwarder.utils.get_config import Config
from timetableforwarder.handlers.routers_for_all.rout_start import start_rout
from aiogram.utils.formatting import Text


def _kb_confirm_mailing() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text="✅ Да", callback_data="mail_yes"),
                          InlineKeyboardButton(text="❌ Нет", callback_data="mail_no")]]
    )


def _kb_return_start() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text="↩ На старт", callback_data="cfg_back")]]
    )


async def mailing_cmd(message: Message, state: FSMContext) -> None:
    await message.answer("Пришлите сообщение для рассылки ✉️")
    await state.set_state(AdminState.waiting_for_mailing)


async def mailing_receive(message: Message, state: FSMContext) -> None:
    await state.update_data(
        from_chat_id=message.chat.id,
        message_to_forward_id=message.message_id
    )
    preview_text = "Это сообщение отправить всем пользователям?"
    await message.answer(preview_text, reply_markup=_kb_confirm_mailing())


async def mailing_send(cb: CallbackQuery, state: FSMContext, users_dao: UsersDAO, config: Config) -> None:
    data = await state.get_data()
    from_chat_id = data.get("from_chat_id") 
    message_to_forward_id = data.get("message_to_forward_id")

    users = await users_dao.get_all_users()
    sent = 0
    for user in users:
        if user.user_id == config.creator_id:
            continue
        try:
            await cb.bot.copy_message(
                chat_id=user.user_id,
                from_chat_id=from_chat_id,
                message_id=message_to_forward_id
            )
        except (TelegramBadRequest, TelegramForbiddenError):
            continue
        else:
            sent += 1

    await cb.message.edit_text(f"<b>Рассылка завершена ✅</b>\n"
                               f"Получили: {sent} юзер(a/ов)\n"
                               f"Не получили: {len(users) - sent} юзер(a/ов)",
                               parse_mode="HTML")
    await cb.message.edit_reply_markup(reply_markup=_kb_return_start())
    await state.clear()
    await cb.answer()


async def mailing_cancel(cb: CallbackQuery, state: FSMContext, users_dao: UsersDAO) -> None:
    await state.clear()
    await start_rout(cb.message, users_dao, called_user=(cb.from_user.id, cb.from_user.username))
    await cb.answer()


