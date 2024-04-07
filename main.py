import asyncio
import logging
import threading
import time

import requests
import telebot
from aiogram import Dispatcher, F
from aiogram.client.default import DefaultBotProperties
from aiogram.filters import CommandStart

from core.db.database_manager import DatabaseManager_thread
from core.forms.forms import *
from core.handlers.callback import *
from core.handlers.command import *
from core.handlers.other import *
from core.handlers.raw_text import *
from core.middlewares.middleware import DatabaseMiddleware


async def start():
    logging.basicConfig(level=logging.INFO,
                        format="%(asctime)s - [%(levelname)s] - %(name)s - (%(filename)s).%"
                               "(funcName)s(%(lineno)d) - %(message)s")

    bot = Bot(token=TELEGRAM_API_TOKEN, default=DefaultBotProperties(parse_mode='HTML'))
    dp = Dispatcher()

    news_polling_thread = threading.Thread(target=news_polling)
    news_polling_thread.start()

    dp.message.middleware(DatabaseMiddleware())
    dp.callback_query.middleware(DatabaseMiddleware())

    dp.message.register(handle_start, CommandStart())
    dp.message.register(set_login, FormLogin.login)
    dp.message.register(set_password, FormLogin.password)

    # callback
    dp.callback_query.register(show_report, F.data == "get_report")
    dp.callback_query.register(get_menu, F.data == "menu")
    dp.callback_query.register(start_login, F.data == "log_in")
    dp.callback_query.register(handle_get_data, F.data == "get_data")
    dp.callback_query.register(handle_add_transaction, F.data == "add_transaction")
    dp.callback_query.register(handle_qr, F.data == "send_QR")
    dp.callback_query.register(handle_deposite_money, F.data == "deposite_money")
    dp.callback_query.register(process_data_navigation, F.data.startswith("page_"))

    # change email
    dp.callback_query.register(handle_change_email, F.data == "change_email")
    dp.message.register(handle_check_password_for_email, ChangeEmail.check_old_password)
    dp.message.register(new_email, ChangeEmail.new_email)

    # change username
    dp.callback_query.register(handle_change_nickname, F.data == 'change_nickname')
    dp.message.register(new_nickname, ChangeNickname.new_nickname)

    # change passwd
    dp.callback_query.register(handle_change_passwd_old, F.data == "change_passwd")
    dp.message.register(handle_check_password_for_password, ChangePassword.check_old_password)
    dp.message.register(new_password, ChangePassword.new_password)

    # transaction
    dp.message.register(set_form_transaction_name, FormTransaction.name)
    dp.message.register(set_from_transaction_quantity, FormTransaction.quantity)
    dp.message.register(set_form_transaction_cost, FormTransaction.cost)
    dp.message.register(set_form_transaction_category, FormTransaction.category)
    dp.message.register(do_file_qr, FormQR.qr)
    dp.message.register(deposite_money_name, FormDepositeMpney.name)
    dp.message.register(deposite_money_sum, FormDepositeMpney.sum)

    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


def news_polling():
    logging.info('News polling started')
    news_api = f'http://{HOST}:{PORT_API}/get_last_news_tg'
    subscribe_api = f"http://{HOST}:{PORT_API}/get_users_subscription?user_id="

    db_manager = DatabaseManager_thread()
    bot = telebot.TeleBot(TELEGRAM_API_TOKEN)

    while True:
        data = json.loads(requests.get(news_api).content.decode('utf-8'))

        if len(data) > 0:
            logging.info('Recent news has been added')

        for elem in data:
            for user_id in db_manager.get_all_users_id():
                user_subs = json.loads(requests.get(subscribe_api + str(user_id)).content.decode('utf-8'))['subs']

                if data[elem]['title'] in user_subs:
                    markup = telebot.types.InlineKeyboardMarkup()
                    markup.add(telebot.types.InlineKeyboardButton(text='Читать полностью',
                                                                url=data[elem]['link']))
                    bot.send_message(chat_id=user_id, text=f"📰Новости от "
                                                        f"{data[elem]['title']}\n\n📌"
                                                        f"{data[elem]['description']}"
                                                        f"\n\n📅{data[elem]['date']}",
                                    reply_markup=markup)
        time.sleep(time_out)


if __name__ == "__main__":
    asyncio.run(start())
