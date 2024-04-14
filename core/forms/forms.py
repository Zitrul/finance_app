from aiogram.fsm.state import State, StatesGroup


class FormLogin(StatesGroup):
    login = State()
    password = State()

class ChangeDeposit(StatesGroup):
    depId = State()
    name = State()
    amount = State()

class FormTransaction(StatesGroup):
    name = State()
    quantity = State()
    cost = State()
    category = State()
    select_category = State()


class FormQR(StatesGroup):
    qr = State()

class FormDepositeMpney(StatesGroup):
    name=State()
    sum = State()

class ChangeNickname(StatesGroup):
    new_nickname = State()



class ChangeEmail(StatesGroup):
    check_old_password = State()
    new_email = State()


class ChangePassword(StatesGroup):
    check_old_password = State()
    # кто читает тот чиназес :3
    new_password = State()
