import os
from telebot.types import Message
import database
from loader import bot
from . import sender
import requests
import json
from . import city_search
from states.low_price import UserInfoState


@bot.message_handler(commands=['low_price'])
def bot_low_price(message: Message):
    city_search.bot_info_city(message)
    bot.set_state(message.from_user.id, UserInfoState.next_low)


@bot.message_handler(state=UserInfoState.next_low)
def bot_next_low_price(message: Message):
    bot.send_message(message.chat.id, "Собираю данные")
    city_search.bot_city(message)
    url = "https://the-fork-the-spoon.p.rapidapi.com/restaurants/v2/list"

    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        querystring = {"queryPlaceValueCityId": data["id_city"],
                       "filterRateStart": "9", "pageSize": "10", "pageNumber": "1",
                       "sort": "-price"}

    headers = {
        "X-RapidAPI-Key": os.getenv("RAPID_API_KEY"),
        "X-RapidAPI-Host": "the-fork-the-spoon.p.rapidapi.com"
    }

    response = json.loads(requests.request("GET", url, headers=headers, params=querystring).text)
    city = response.get("meta").get("city").get("name")
    if len(response.get("data", [])) > 0 and type(response.get("data", 0)) == list:
        response = sorted(response["data"],
                          key=lambda x: (
                              x.get("priceRange", 0),
                              -x.get("aggregateRatings", 0).get("thefork", 0).get("ratingValue", 0),
                              -x.get("aggregateRatings", 0).get("thefork", 0).get("reviewCount", 0)))
        response = tuple([x for x in response if x["priceRange"] != 0])
        bot.send_message(message.chat.id, "Готово")

        database.record(response, "/low_price", message.chat.id, city)
        sender.bot_quest(message, response, 10)
    else:
        bot.send_message(message.from_user.id, "Не было найдено подходящих ресторанов")
