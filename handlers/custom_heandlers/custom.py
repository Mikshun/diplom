import os
from telebot.types import Message
import database
from loader import bot
from . import sender
import requests
import json
from states.custom_request import UserInfoState
from . import city_search


@bot.message_handler(commands=['custom'])
def bot_custom(message: Message):
    city_search.bot_info_city(message)
    bot.set_state(message.from_user.id, UserInfoState.next_custom)


@bot.message_handler(state=UserInfoState.next_custom)
def bot_custom(message: Message):
    bot.send_message(message.from_user.id, "Подгружаю данные")
    city_search.bot_city(message)
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        if data["id_city"] is None:
            return
    bot.send_message(message.from_user.id, "Введи пожалуйста в виде числа минимальную цену в евро")
    bot.set_state(message.from_user.id, UserInfoState.min_price)


@bot.message_handler(state=UserInfoState.min_price)
def bot_min_rate(message: Message):
    if message.text.isnumeric():
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data["min_price"] = message.text
        bot.send_message(message.from_user.id, "Записал, теперь введите в виде числа  максимальную цену в евро")
        bot.set_state(message.from_user.id, UserInfoState.max_price)
    else:
        bot.reply_to(message.from_user.id, "Вы ввели не число")


@bot.message_handler(state=UserInfoState.max_price)
def bot_max_rate(message: Message):
    if message.text.isnumeric():
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data["max_price"] = message.text
        bot.send_message(message.from_user.id, "Записал, введите пожалуйста минимальный рейтинг в виде числа до 10")
        bot.set_state(message.from_user.id, UserInfoState.min_rate)
    else:
        bot.reply_to(message.from_user.id, "Вы ввели не число")


@bot.message_handler(state=UserInfoState.min_rate)
def bot_max_rate(message: Message):
    if message.text.isnumeric() and int(message.text) <= 10:
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data["min_rate"] = message.text
        bot.send_message(message.from_user.id,
                         "Записал, последнее сколько результатов отображать на странице введите числом до 10")
        bot.set_state(message.from_user.id, UserInfoState.pageSize)
    else:
        bot.reply_to(message.from_user.id, "Вы ввели не число или цифра была больше 10")


@bot.message_handler(state=UserInfoState.pageSize)
def bot_max_rate(message: Message):
    if message.text.isnumeric() and int(message.text) <= 20:
        bot.set_state(message.from_user.id, state=None)
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data["pageSize"] = message.text
        bot.send_message(message.chat.id, "Собираю данные")

        if data["id_city"] is None:
            return

        url = "https://the-fork-the-spoon.p.rapidapi.com/restaurants/v2/list"

        querystring = {"queryPlaceValueCityId": data["id_city"], "filterRateStart": data["min_rate"],
                       "filterPriceEnd": data["max_price"], "filterPriceStart": data["min_price"],
                       "pageSize": data["pageSize"], "pageNumber": "1"}

        headers = {
            "X-RapidAPI-Key": os.getenv("RAPID_API_KEY"),
            "X-RapidAPI-Host": "the-fork-the-spoon.p.rapidapi.com"
        }

        response = json.loads(requests.request("GET", url, headers=headers, params=querystring).text)
        city = response.get("meta").get("city").get("name")
        if len(response.get("data", [])) > 0 and type(response.get("data", 0)) == list:
            response = sorted(response["data"],
                              key=lambda x: (x.get("priceRange", 0),
                                             -x.get("aggregateRatings", 0).get("thefork", 0).get("ratingValue", 0),
                                             -x.get("aggregateRatings", 0).get("thefork", 0).get("reviewCount", 0)))
            response = tuple([x for x in response if x["priceRange"] != 0])
            bot.send_message(message.chat.id, "Готово")

            database.record(response, '/custom', message.chat.id, city)
            sender.bot_quest(message, response, int(data["pageSize"]))
        else:
            bot.send_message(message.from_user.id, "Не было найдено подходящих ресторанов")
    else:
        bot.reply_to(message.from_user.id, "Вы ввели не целое число или цифра была больше 10")
