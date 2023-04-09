from telebot.handler_backends import State, StatesGroup


class UserInfoState(StatesGroup):
    next_low = State()