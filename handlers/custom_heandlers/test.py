
from telebot.types import Message
from database import orm
from loader import bot


@bot.message_handler(commands=['test'])
def bot_test(message: Message):
    orm.record(message)
    bot.send_message(message.chat.id, "Сделал запись в таблицу данных.")
