import json
import peewee
from telebot.types import Message
import database
from keyboards.reply.yas_no import yas_no_button
from loader import bot
from . import sender
from states.need_result import UserInfoState


def standart_text(users_list: peewee.Model) -> str:
    basic_text = "Используемая команда: {command}\n" \
                 "Город поиска: {city}\n" \
                 "Дата и время команды: {date} {time}\n".format(command=users_list.command,
                                                                city=users_list.city,
                                                                date=users_list.request_date,
                                                                time=users_list.request_time)
    return basic_text


@bot.message_handler(commands=['history'])
def bot_need_history(message: Message):
    bot.set_state(message.from_user.id, UserInfoState.need_result)
    bot.send_message(message.from_user.id, "Вывести ли результаты команд из истории? да/нет", reply_markup=yas_no_button())


@bot.message_handler(state=UserInfoState.need_result)
def bot_show_history(message: Message):
    if message.text.lower() == 'да':
        bot.set_state(message.from_user.id, UserInfoState.photo)
        bot.send_message(message.from_user.id, "Вам нужны фото ресторанов? да/нет", reply_markup=yas_no_button())

    elif message.text.lower() == 'нет':
        for i in database.User.select().where(database.User.user_id == message.chat.id).order_by(database.User.id):
            bot.send_message(message.from_user.id, standart_text(i))
            bot.set_state(message.from_user.id, state=None)
    else:
        bot.send_message(message.from_user.id, "Нужно ответить да или нет")


@bot.message_handler(state=UserInfoState.photo)
def bot_show_history_with_photo(message: Message):
    if message.text.lower() == 'да':
        for i in database.User.select().where(database.User.user_id == message.chat.id).order_by(database.User.id):
            bot.send_message(message.from_user.id, f"{standart_text(i)}\n Результаты:")
            for results in json.loads(i.result):
                if type(results.get("mainPhoto")) == dict and len(results.get("mainPhoto")) > 0:
                    for photo in results.get("mainPhoto"):
                        try:
                            bot.send_photo(message.from_user.id, results["mainPhoto"][photo], caption=sender.text_example(results))
                            break
                        except:
                            bot.send_message(message.from_user.id, "Не удалось загрузить фото, загружаю другое")
    elif message.text.lower() == 'нет':
        for i in database.User.select().where(database.User.user_id == message.chat.id).order_by(database.User.id):
            bot.send_message(message.from_user.id, f"{standart_text(i)}\n Результаты:")
            for results in json.loads(i.result):
                bot.send_message(message.from_user.id, sender.text_example(results))
    else:
        bot.send_message(message.from_user.id, "Нужно ответить да или нет")
