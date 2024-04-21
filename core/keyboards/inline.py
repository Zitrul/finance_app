from aiogram.utils.keyboard import InlineKeyboardBuilder


def get_log_in_keyboard():
    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.button(text="Войти по логину / паролю", callback_data="log_in")
    return keyboard_builder.as_markup()

def get_change_transaction_keyboard():
    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.button(text='Изменить', callback_data='change_transaction_start')
    keyboard_builder.button(text="↩️ Назад", callback_data="menu")
    return keyboard_builder.adjust(1, 1).as_markup()


def get_change_deposit_keyboard():
    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.button(text="Изменить", callback_data='change_deposite_start')
    keyboard_builder.button(text="↩️ Назад", callback_data="menu")
    return keyboard_builder.adjust(1, 1).as_markup()

def get_change_money_info_keyboard():
    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.button(text="Изменить доходы", callback_data='change_deposite')
    keyboard_builder.button(text="Изменить траты", callback_data="change_transaction")
    keyboard_builder.button(text="↩️ Назад", callback_data="menu")
    return keyboard_builder.adjust(1, 1).as_markup()

def get_main_menu_keyboard():
    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.button(text="👤 Мои данные", callback_data="get_data")
    keyboard_builder.button(text="🛒 Добавить транзакцию", callback_data="add_transaction")
    keyboard_builder.button(text="🧾 Отправить QR", callback_data="send_QR")
    keyboard_builder.button(text="🗂 Транзакции", callback_data='page_next_0')
    keyboard_builder.button(text="💹 Внести ЗП", callback_data="deposite_money")
    keyboard_builder.button(text="✏ Затраты / Доходы", callback_data="change_money_info")
    keyboard_builder.button(text='📄 Отчет', callback_data='get_report')
    keyboard_builder.button(text='📈 График трат', callback_data='get_visuals')
    keyboard_builder.button(text='💸 Продать акции', callback_data='sell_shares')
    return keyboard_builder.adjust(2, repeat=True).as_markup()


def get_about_menu_keyboard():
    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.button(text='✏️ Изменить никнейм', callback_data='change_nickname')
    keyboard_builder.button(text='✏️ Изменить пароль', callback_data='change_passwd')
    keyboard_builder.button(text='✏️ Изменить почту', callback_data='change_email')
    keyboard_builder.button(text='↩️ Назад', callback_data='menu')
    return keyboard_builder.adjust(1, 1).as_markup()


def get_return_keyboard():
    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.button(text='↩️ Назад', callback_data='menu')
    return keyboard_builder.as_markup()
