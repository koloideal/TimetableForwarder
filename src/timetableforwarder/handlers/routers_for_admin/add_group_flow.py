import re
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from timetableforwarder.states.admin_states import AdminState
from timetableforwarder.utils.config_editor import add_group


async def add_group_cmd(message: Message, state: FSMContext) -> None:
    await message.answer("Введите номер группы (4 цифры) ✍️")
    await state.set_state(AdminState.waiting_for_add_group)


async def add_group_receive(message: Message, state: FSMContext) -> None:
    text = (message.text or "").strip()
    if not re.fullmatch(r"\d{4}", text):
        await message.answer("Неверный формат ⚠️\nВведите 4 цифры, например 1125")
        return
    group_id = int(text)
    ok = add_group(group_id)
    if ok:
        await message.answer(f"Группа {group_id} добавлена ✅")
    else:
        await message.answer(f"Группа {group_id} уже существует 🔁")
    await state.clear()


