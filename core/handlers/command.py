from aiogram import Bot
from aiogram.enums.parse_mode import ParseMode
from aiogram.types import Message

from core.db.database_manager import DatabaseManager
from core.keyboards.inline import get_log_in_keyboard, get_main_menu_keyboard


async def handle_start(message: Message, bot: Bot, db_manager: DatabaseManager):
    if not await db_manager.is_user_by_telegram_id(message.chat.id):
        if start_data := message.text.split('/start')[1].strip():
            if await db_manager.update_user_token(message.from_user.id, start_data):
                await bot.send_message(message.chat.id, f"Успешная привязка!")
                await bot.send_message(message.chat.id, f"「📂」 <b>Меню</b>",
                                       reply_markup=get_main_menu_keyboard(),
                                       parse_mode=ParseMode.HTML)
            else:
                await bot.send_message(message.chat.id, f"Такой токен не обнаружен. Нажмите кнопку "
                                                        "ниже, для входа по логину и паролю.",
                                       reply_markup=get_log_in_keyboard())
        else:
            await bot.send_message(message.chat.id, "Вы не зарегистрированы. Используйте токен или нажмите кнопку "
                                                    "ниже, для входа по логину и паролю.",
                                   reply_markup=get_log_in_keyboard())
    else:
        await bot.send_message(message.chat.id, f"「📂」 <b>Меню</b>",
                               reply_markup=get_main_menu_keyboard(),
                               parse_mode=ParseMode.HTML)
