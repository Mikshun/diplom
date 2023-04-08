import os
from telebot.types import Message
import database
from loader import bot
from . import sender
import requests
import json


@bot.message_handler(commands=['low_price'])
def bot_low_price(message: Message):
    bot.send_message(message.chat.id, "Собираю данные")
    url = "https://the-fork-the-spoon.p.rapidapi.com/restaurants/v2/list"

    querystring = {"queryPlaceValueCityId": "348156", "filterRateStart": "9", "pageSize": "10", "pageNumber": "1",
                   "sort": "-price"}

    headers = {
        "X-RapidAPI-Key": os.getenv("RAPID_API_KEY"),
        "X-RapidAPI-Host": "the-fork-the-spoon.p.rapidapi.com"
    }

    response = json.loads(requests.request("GET", url, headers=headers, params=querystring).text)
    if len(response.get("data", [])) > 0 and type(response.get("data", 0)) == list:
        response = sorted(response["data"],
                          key=lambda x: (
                          x.get("priceRange", 0), -x.get("aggregateRatings", 0).get("thefork", 0).get("ratingValue", 0),
                          -x.get("aggregateRatings", 0).get("thefork", 0).get("reviewCount", 0)))
        response = tuple([x for x in response if x["priceRange"] != 0])
        bot.send_message(message.chat.id, "Готово")

        database.record(response, message.text, message.chat.id)
        sender.bot_quest(message, response, 10)
    else:
        bot.send_message(message.from_user.id, "Не было найдено подходящих ресторанов")
