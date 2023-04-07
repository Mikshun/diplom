from telebot.handler_backends import State, StatesGroup


class UserInfoState(StatesGroup):
    need_result = State()
    photo = State()
