import json

import aiohttp
from aiogram import Bot
from aiogram.enums.parse_mode import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, FSInputFile
import matplotlib.pyplot as plt
from telebot.types import InputFile

from core.db.database_manager import DatabaseManager
from core.forms.forms import *
from core.keyboards.inline import *
from core.settings import HOST, PORT_API


async def start_login(callback: CallbackQuery, state: FSMContext, bot: Bot):
    await callback.answer()
    await bot.send_message(callback.message.chat.id, f"Введите ваш login:")
    await state.set_state(FormLogin.login)

async def show_report(callback: CallbackQuery, bot : Bot, db_manager : DatabaseManager):
    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.button(text='↩️ В меню', callback_data='menu')
    await bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.message_id, text=f'Всего трат: {sum(await db_manager.get_all_transaction_amount(callback.from_user.id))} RUB\nСтоимость акций: {await db_manager.get_all_amount_share(callback.from_user.id)} RUB\nВсего заработано: {await db_manager.get_all_amount_salary(callback.from_user.id)} RUB\nБаланс: {await db_manager.get_all_amount_salary(callback.from_user.id) + await db_manager.get_all_amount_share(callback.from_user.id) - sum(await db_manager.get_all_transaction_amount(callback.from_user.id))} RUB', reply_markup=keyboard_builder.as_markup())

async def delete_share_start(callback : CallbackQuery, bot : Bot, state : FSMContext):
    await callback.answer()
    await bot.send_message(text='Введите ID:', chat_id=callback.message.chat.id)
    await state.set_state(DeleteShare.share_id)

async def handle_delete_share(callback : CallbackQuery, bot : Bot, db_manager : DatabaseManager):
    await callback.answer()
    text = ''
    for elem in await db_manager.get_all_share(callback.from_user.id):
        text += str(elem) + '\n'
    if text == '':
        text = 'Нету акций!'
    await bot.edit_message_text(text=text, message_id=callback.message.message_id, chat_id=callback.message.chat.id, reply_markup=get_delete_share_keyborad())

async def handle_start_change_transaction(callback : CallbackQuery, bot : Bot, state : FSMContext):
    await callback.answer()
    await bot.send_message(chat_id=callback.message.chat.id, text='Введите ID:')
    await state.set_state(ChangeTransaction.trnId)

async def change_deposit_start(callback : CallbackQuery, bot: Bot, state : FSMContext):
    await callback.answer()
    await bot.send_message(chat_id=callback.message.chat.id, text='Введите ID:')
    await state.set_state(ChangeDeposit.depId)

async def change_transaction(callback : CallbackQuery, bot : Bot, db_manager : DatabaseManager):
    await callback.answer()
    text = '////'
    # for elem in await db_manager.get_transactions(callback.from_user.id):
    #     text += str(elem) + '\n'
    #print(text)
    await bot.edit_message_text(chat_id=callback.message.chat.id,
                                text = text,
                                message_id=callback.message.message_id,
                                reply_markup=get_change_transaction_keyboard())

async def change_deposit(callback : CallbackQuery, bot : Bot, db_manager : DatabaseManager):
    await callback.answer()
    text = ''
    for elem in await db_manager.get_all_salary(callback.from_user.id):
        text += str(elem) + '\n'
    
    await bot.edit_message_text(chat_id=callback.message.chat.id,
                                message_id=callback.message.message_id,
                                text=text,
                                reply_markup=get_change_deposit_keyboard())

async def handle_qr(callback: CallbackQuery, state: FSMContext, bot: Bot):
    await callback.answer()
    await bot.send_message(callback.message.chat.id, f"Отправьте фото:")
    await state.set_state(FormQR.qr)

async def handle_deposite_money(callback: CallbackQuery, state: FSMContext, bot: Bot):
    await callback.answer()
    await bot.send_message(callback.message.chat.id, f"Введите комментарий по доходу:")
    await state.set_state(FormDepositeMpney.name)

async def handle_sell_shares(callback: CallbackQuery, state: FSMContext, bot: Bot):
    await callback.answer()
    await bot.send_message(callback.message.chat.id, f"Введите название акций:")
    await state.set_state(FormSellShares.ticker)

async def change_money_info(callback : CallbackQuery, bot : Bot):
    await callback.answer()
    await bot.edit_message_text(chat_id=callback.message.chat.id,
                                message_id=callback.message.message_id,
                                text=f"「📂」 <b>Что хотите поменять?</b>",
                                reply_markup=get_change_money_info_keyboard(),
                                parse_mode=ParseMode.HTML)

async def get_menu(callback: CallbackQuery, bot: Bot):
    await callback.answer()
    await bot.edit_message_text(chat_id=callback.message.chat.id,
                                message_id=callback.message.message_id,
                                text=f"「📂」 <b>Меню</b>",
                                reply_markup=get_main_menu_keyboard(),
                                parse_mode=ParseMode.HTML)


async def handle_change_nickname(callback: CallbackQuery, bot: Bot, db_manager: DatabaseManager, state: FSMContext):
    await callback.answer()
    await bot.send_message(text='Введите новый никнейм:', chat_id=callback.message.chat.id)
    await state.set_state(ChangeNickname.new_nickname)


async def handle_change_passwd_old(callback: CallbackQuery, bot: Bot, db_manager: DatabaseManager, state: FSMContext):
    await callback.answer()
    await bot.send_message(text='Введите свой старый пароль:', chat_id=callback.message.chat.id)
    await state.set_state(ChangePassword.check_old_password)


async def handle_get_transactions(callback: CallbackQuery, bot: Bot, db_manager: DatabaseManager):
    await callback.answer()
    transactions_list = await db_manager.get_transactions(callback.message.chat.id)
    msg = ''
    for transaction in transactions_list:
        msg += f'ID: {transaction[0]}\nName: {transaction[1]}\nAmount: {transaction[2]}\nCategory: {transaction[3]}\n\n___________________________\n'
    await bot.send_message(callback.message.chat.id, text=msg)


async def handle_get_data(callback: CallbackQuery, bot: Bot, db_manager: DatabaseManager):
    await callback.answer()
    data = await db_manager.get_user_by_telegram_id(callback.from_user.id)
    await bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.message_id,
                                text=f"「👤」 <b>Ваши данные:</b>\n"
                                     f"──────────────\n"
                                     f"<b>Имя:</b> {data['first_name']} {data['last_name']}\n"
                                     f"<b>Никнейм:</b> {data['username']}\n"
                                     f"<b>Телефон:</b> {data['telephone_number']}\n"
                                     f"<b>Почта:</b> {data['email_auth']}\n"
                                     f"<b>Дата создания:</b> {data['created_at']}",
                                reply_markup=get_about_menu_keyboard())


async def process_data_navigation(callback: CallbackQuery, bot: Bot, db_manager: DatabaseManager):  # page_next_1
    page_data = callback.data.split("_")
    direction, page_number = page_data[1], int(page_data[2])

    content = f"「💸」 <b>Последние транзакции:</b>\n" \
              f"──────────────\n"

    data = await db_manager.get_transactions(callback.message.chat.id)
    data = data[::-1]

    page_size = 5
    if direction == 'prev':
        page_number -= 1
    elif direction == 'next':
        page_number += 1

    start_index = (page_number - 1) * page_size
    end_index = min(start_index + page_size, len(data))

    chunk = data[start_index:end_index]

    keyboard_builder = InlineKeyboardBuilder()
    button_cnt = 0
    if start_index > 0:
        keyboard_builder.button(text="◀️ Предыдущая", callback_data=f"page_prev_{page_number}")
        button_cnt += 1
    if end_index < len(data):
        keyboard_builder.button(text="Следующая ▶️", callback_data=f"page_next_{page_number}")
        button_cnt += 1

    for transaction in chunk:
        content += f'<b>ID:</b> {transaction[0]}\n<b>Имя:</b> {transaction[1]}\n<b>Стоимость:</b> {transaction[2]} RUB\n' \
                   f'<b>Категория:</b> {transaction[3]}\n──────────────\n'

    keyboard_builder.button(text='↩️ В меню', callback_data='menu')

    if button_cnt == 2:
        keyboard_builder.adjust(2, 1)
    else:
        keyboard_builder.adjust(1, 1)

    await bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.message_id,
                                text=content, reply_markup=keyboard_builder.as_markup())

    await callback.answer()


async def handle_add_transaction(callback: CallbackQuery, state: FSMContext, bot: Bot):
    await callback.answer()
    await bot.send_message(callback.message.chat.id, '[1/4] Введите <b>название</b> товара:')
    await state.set_state(FormTransaction.name)


async def handle_show_visuals(callback: CallbackQuery, state: FSMContext, bot: Bot, db_manager: DatabaseManager):
    await callback.answer()

    user_id = (await db_manager.get_user_by_telegram_id(callback.from_user.id))['id']
    cur_date = "2024-04-01"

    api_request = f"http://{HOST}:{PORT_API}/get_transactions_by_date?user_id={user_id}&datefrom={cur_date}"

    async with aiohttp.ClientSession() as session:
        async with session.get(api_request) as resp:
            data = json.loads((await resp.text()))

    dates = list(data.keys())
    values = list(data.values())

    plt.figure(figsize=(10, 6))
    plt.plot(dates, values, marker='o')
    plt.xlabel('Дата')
    plt.ylabel('Траты')
    plt.title(f'График трат от {cur_date}')
    plt.grid(True)
    plt.xticks(rotation=45)

    plt.savefig('plot.png')  # Сохраняем график как изображение

    chat_id = callback.message.chat.id
    await bot.send_photo(chat_id, FSInputFile("plot.png"))

