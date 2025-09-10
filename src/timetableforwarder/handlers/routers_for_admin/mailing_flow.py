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
    has_photo = bool(message.photo)
    text = message.text if message.text is not None else None
    entities = message.entities if message.entities is not None else None
    caption = message.caption if message.caption is not None else None
    caption_entities = message.caption_entities if message.caption_entities is not None else None
    photo_file_id = message.photo[-1].file_id if has_photo else None

    text_html = Text(text, entities=entities).as_html() if text is not None else None
    caption_html = Text(caption, entities=caption_entities).as_html() if caption is not None else None

    await state.update_data(
        has_photo=has_photo,
        text_html=text_html,
        caption_html=caption_html,
        photo_file_id=photo_file_id,
    )
    preview_text = "Это сообщение отправить всем пользователям?"
    await message.answer(preview_text, reply_markup=_kb_confirm_mailing())


async def mailing_send(cb: CallbackQuery, state: FSMContext, users_dao: UsersDAO, config: Config) -> None:
    data = await state.get_data()
    has_photo = data.get("has_photo", False)
    text_html = data.get("text_html")
    caption_html = data.get("caption_html")
    photo_file_id = data.get("photo_file_id")

    users = await users_dao.get_all_users()
    sent = 0
    for user in users:
        if user.user_id == config.creator_id:
            continue
        try:
            if has_photo and photo_file_id:
                await cb.bot.send_photo(
                    chat_id=user.user_id,
                    photo=photo_file_id,
                    caption=caption_html,
                    parse_mode="HTML",
                )
            else:
                if text_html:
                    await cb.bot.send_message(
                        chat_id=user.user_id,
                        text=text_html,
                        parse_mode="HTML",
                    )
            sent += 1
        except (TelegramBadRequest, TelegramForbiddenError):
            continue

    await cb.message.edit_text(f"Рассылка завершена ✅ Отправлено: {sent}")
    await cb.message.edit_reply_markup(reply_markup=_kb_return_start())
    await state.clear()
    await cb.answer()


async def mailing_cancel(cb: CallbackQuery, state: FSMContext, users_dao: UsersDAO) -> None:
    await state.clear()
    await start_rout(cb.message, users_dao, called_user=(cb.from_user.id, cb.from_user.username))
    await cb.answer()


