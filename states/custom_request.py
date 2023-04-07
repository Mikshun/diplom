from telebot.handler_backends import State, StatesGroup


class UserInfoState(StatesGroup):
    min_rate = State()
    min_price = State()
    max_price = State()
    pageSize = State()
