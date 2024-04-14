import json
import re

import aiohttp
import bcrypt
from aiogram import Bot
from aiogram.enums.parse_mode import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from aiogram.types import Message

from core.db.database_manager import DatabaseManager
from core.forms.forms import *
from core.keyboards.inline import get_log_in_keyboard, get_main_menu_keyboard
from core.keyboards.inline import get_return_keyboard
from core.settings import HOST, PORT_API, encoding, CATEGORIES


async def set_form_transaction_name(message: Message, state: FSMContext, bot: Bot):
    await state.update_data(name=message.text)
    await bot.send_message(message.chat.id, "[2/4] Введите <b>количество</b> товара:")
    await state.set_state(FormTransaction.quantity)


async def set_from_transaction_quantity(message: Message, state: FSMContext, bot: Bot):
    await state.update_data(quantity=message.text)
    await bot.send_message(message.chat.id, '[3/4] Введите всю <b>стоимость</b>:')
    await state.set_state(FormTransaction.cost)


async def set_form_transaction_cost(message: Message, state: FSMContext, bot: Bot):
    await state.update_data(cost=message.text)

    content = "[4/4] Выберите <b>категорию</b> (или напишите свою):\n\n"

    for num, category in enumerate(CATEGORIES):
        content += f"/_{num+1}_. <b>{category}</b>\n"

    await bot.send_message(message.chat.id, content)
    await state.set_state(FormTransaction.category)


async def set_form_transaction_category(message: Message, state: FSMContext, bot: Bot, db_manager: DatabaseManager):
    if "_" in message.text:
        cur = CATEGORIES[int(message.text.split("_")[1]) - 1]
        await state.update_data(category=cur)
        select_category = False
    else:
        await state.update_data(category=message.text)
        select_category = False
    data = await state.get_data()

    user_id = await db_manager.get_user_by_telegram_id(message.from_user.id)
    user_id = user_id['id']

    api_request = f"http://{HOST}:{PORT_API}/add_product_user?user_id={user_id}&name={data['name']}&amount=" \
                  f"{data['cost']}&currency=RUB&select_category={select_category}&category={data['category']}"

    async with aiohttp.ClientSession() as session:
        async with session.post(api_request) as resp:
            status = 1 if json.loads(await resp.text())['OK'] == 'OK' else 0

    if status:
        await bot.send_message(message.chat.id, '「✅」 Добавление транзакции прошло успешно!',
                               reply_markup=get_return_keyboard())
    else:
        await bot.send_message(message.chat.id, 'Ошибка! Попробуйте еще раз!')
    await state.clear()

async def deposite_money_name(message: Message, state: FSMContext, bot: Bot, db_manager: DatabaseManager):
    await state.update_data(name=message.text)
    await bot.send_message(message.chat.id, "Введите сумму дохода:")
    await state.set_state(FormDepositeMpney.sum)



async def deposite_money_sum(message: Message, state: FSMContext, bot: Bot, db_manager: DatabaseManager):
    try:
        money = int(message.text)
    except:
        await state.clear()
        await bot.send_message(message.chat.id, "Вы ввели неправильные данные")
        return

    user_id = await db_manager.get_user_by_telegram_id(message.from_user.id)
    user_id = user_id['id']

    data = await state.get_data()

    api_request = f"http://{HOST}:{PORT_API}/add_profit_transaction?user_id={user_id}&" \
                  f"name={data['name']}&category=Работа&amount={money}"

    async with aiohttp.ClientSession() as session:
        async with session.post(api_request) as resp:
            status = 1 if json.loads(await resp.text())['OK'] == 'OK' else 0

    if status:
        await bot.send_message(message.chat.id, '「✅」 Добавление дохода прошло успешно!',
                               reply_markup=get_return_keyboard())
    else:
        await bot.send_message(message.chat.id, 'Ошибка! Попробуйте еще раз!')
    await state.clear()



async def set_login(message: Message, state: FSMContext, bot: Bot):
    await state.update_data(login=message.text)
    await bot.send_message(message.chat.id, "Теперь введите ваш пароль: ")
    await state.set_state(FormLogin.password)


async def new_nickname(message: Message, state: FSMContext, bot: Bot, db_manager: DatabaseManager):
    await state.update_data(new_nickname=message.text.strip())
    data = await state.get_data()
    await db_manager.insert_user_info(message.from_user.id, 'username', data['new_nickname'])
    await bot.send_message(text='「✅」  Данные успешно обновлены!', chat_id=message.chat.id)
    await state.clear()


async def new_password(message: Message, state: FSMContext, bot: Bot, db_manager: DatabaseManager):
    await state.update_data(new_password=message.text.strip())
    bc_salt = bcrypt.gensalt()
    await db_manager.insert_user_info(message.chat.id, 'password',
                                      bcrypt.hashpw(message.text.strip().encode(encoding), bc_salt))
    await bot.send_message(message.chat.id, '「✅」  Пароль успешно изменён!')


async def handle_change_email(callback: CallbackQuery, state: FSMContext, bot: Bot):
    await state.set_state(ChangeEmail.check_old_password)
    await bot.send_message(callback.message.chat.id, 'Введите пароль:')
    await callback.answer()


async def new_email(message: Message, state: FSMContext, bot: Bot, db_manager: DatabaseManager):
    await state.update_data(new_password=message.text.strip())
    pattern = "[a-z0-9!#$%&'+/=?^_`{|}~-]+(?:.[a-z0-9!#$%&'+/=?^_`{|}~-]+)@(?:[a-z0-9](?:[a-z0-9-][a-z0-9]" \
              ")?.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?$"
    if re.match(pattern, message.text.strip()):
        await bot.send_message(message.chat.id, '「✅」  Почта обновлена успешно!')
        await db_manager.insert_user_info(message.chat.id, 'email_auth', message.text.strip())
    else:
        await bot.send_message(message.chat.id, 'Неверный формат почты!')
    await state.clear()

async def handle_change_deposit_amount(message : Message, state : FSMContext, bot : Bot, db_manager : DatabaseManager):
    await state.update_data(amount = message.text.strip())
    dep_id, name, amount = await state.get_data()
    await db_manager.change_deposit(dep_id, name, amount)
    await bot.send_message(message.chat.id, 'изменено!')

async def handle_change_deposit_name(message : Message, state : FSMContext, bot : Bot):
    await state.update_data(name = message.text.strip())
    await bot.send_message(message.chat.id, 'Введите сумму')
    await state.set_state(ChangeDeposit.amount)

async def handle_change_deposit_id(message : Message, state : FSMContext, bot : Bot):
    await state.update_data(depId = message.text.strip())
    await bot.send_message(message.chat.id, 'Введите название:')
    await state.set_state(ChangeDeposit.name)


async def handle_check_password_for_email(message: Message, state: FSMContext, bot: Bot, db_manager: DatabaseManager):
    await state.update_data(old_pas_input=message.text.strip())
    if await db_manager.check_password(message.chat.id, message.text.strip()):
        await bot.send_message(message.chat.id, text='Верно! Введите новую почту:')
        await state.set_state(ChangeEmail.new_email)
    else:
        await bot.send_message(message.chat.id, 'Неверный пароль!')
        await state.clear()


async def handle_check_password_for_password(message: Message, state: FSMContext, bot: Bot,
                                             db_manager: DatabaseManager):
    await state.update_data(old_pas_input=message.text.strip())
    if await db_manager.check_password(message.chat.id, message.text.strip()):
        await bot.send_message(message.chat.id, text='Верно! Введите новый пароль:')
        await state.set_state(ChangePassword.new_password)
    else:
        await bot.send_message(message.chat.id, 'Неверный пароль!')
        await state.clear()


async def set_password(message: Message, state: FSMContext, bot: Bot, db_manager: DatabaseManager):
    await state.update_data(password=message.text)
    data = await state.get_data()

    if token := await db_manager.get_token_by_login_password(data['login'], data['password']):
        if await db_manager.update_user_token(message.from_user.id, token):
            await bot.send_message(message.chat.id, f"Успешная привязка!")
            await bot.send_message(message.chat.id, f"<b>Меню</b>",
                                   reply_markup=get_main_menu_keyboard(),
                                   parse_mode=ParseMode.HTML)
        else:
            await bot.send_message(message.chat.id, f"Увы, такого пользователя не существует. Попробуйте еще раз.",
                                   reply_markup=get_log_in_keyboard())
    else:
        await bot.send_message(message.chat.id, f"Увы, такого пользователя не существует / пароль неверен. "
                                                f"Попробуйте еще раз.",
                               reply_markup=get_log_in_keyboard())
    await state.clear()
