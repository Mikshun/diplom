from telebot.types import Message
from loader import bot


@bot.message_handler(commands=['start'])
def bot_start(message: Message):
    bot.reply_to(message, f"Привет,\n"
                              f"Я помогу вам подобрать лучшие рестораны Милана\n"
                              f"Команды вы можете увидеть благодаря функции /help или слева от поля ввода в кнопочке меню)")


