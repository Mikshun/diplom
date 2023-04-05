
from telebot.types import Message
import database
from loader import bot


@bot.message_handler(commands=['test'])
def bot_test(message: Message):
    id=message.chat.id
    database.record(message.text,id)
    bot.send_message(message.chat.id, "Сделал запись в таблицу данных.")