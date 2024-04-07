import os

from aiogram import Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from core.db.database_manager import DatabaseManager
from core.keyboards.inline import get_return_keyboard
from core.settings import *
from core.utils.api import post_image_async


async def do_file_qr(message: Message, bot: Bot, state: FSMContext, db_manager: DatabaseManager):
    photo_id = message.photo[-1].file_id
    photo = await bot.get_file(photo_id)
    photo_path = photo.file_path
    local_path = os.path.join('temp', f'{message.from_user.id}.png')
    await bot.download_file(photo_path, local_path)

    user_data = await db_manager.get_user_by_telegram_id(message.from_user.id)
    r = await post_image_async(
        url=f"http://{HOST}:{PORT_API}/check_check",
        file_path=local_path,
        values={
            'sort': 'True',
            'user_id': user_data['id']
        }
    )
    content = r[9:-2]
    if content == "QR code прочитан":
        content = "「✅」  " + content
    else:
        content = "「❌」  " + content
    await bot.send_message(message.chat.id, content,
                           reply_markup=get_return_keyboard())
    await state.clear()
