from telebot.types import ReplyKeyboardMarkup, KeyboardButton


def yas_no_button():
    keyboard = ReplyKeyboardMarkup(True, True)
    keyboard.add(KeyboardButton("Да"), KeyboardButton("Нет"))
    return keyboard
