import json
from telebot.types import Message
from loader import bot
import requests


def bot_info_city(message: Message) -> None:
    bot.send_message(message.from_user.id, "Введи пожалуйста город, в котором будем искать рестораны на английском.")


def bot_city(message: Message) -> None:
    city_name = [True if 96 < ord(x.lower()) < 123 else False for x in message.text]
    if all(city_name):
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['city'] = message.text
        url = "https://the-fork-the-spoon.p.rapidapi.com/locations/v2/auto-complete"

        querystring = {"text": message.text}

        headers = {
            "X-RapidAPI-Key": "ec5e4e5dc5mshcefae74201ef905p17df24jsn4bc553c6e182",
            "X-RapidAPI-Host": "the-fork-the-spoon.p.rapidapi.com"
        }

        response = json.loads(requests.request("GET", url, headers=headers, params=querystring).text)

        google_id = response.get("data", None).get("geolocation", None)
        if google_id is not None and len(google_id) > 0:
            google_id = google_id[0].get("id", None).get("id", None)
            if google_id is not None:
                url = "https://the-fork-the-spoon.p.rapidapi.com/locations/v2/list"

                querystring = {"google_place_id": google_id, "geo_ref": "false"}

                headers = {
                    "X-RapidAPI-Key": "ec5e4e5dc5mshcefae74201ef905p17df24jsn4bc553c6e182",
                    "X-RapidAPI-Host": "the-fork-the-spoon.p.rapidapi.com"
                }

                response = json.loads(requests.request("GET", url, headers=headers, params=querystring).text)
                if response.get("id_city", None) is not None:
                    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
                        data['id_city'] = response["id_city"]
                else:
                    bot.send_message(message.from_user.id, "По данному городу к сожалению нет информации")
                    bot.set_state(message.from_user.id, state=None)
            else:
                bot.send_message(message.from_user.id, "По данному городу к сожалению нет информации")
                bot.set_state(message.from_user.id, state=None)
        else:
            bot.send_message(message.from_user.id, "По данному городу к сожалению нет информации")
            bot.set_state(message.from_user.id, state=None)
    else:
        bot.send_message(message.from_user.id,
                         "В сообщении есть недопустимые буквы/символы попробуйте снова, пожалуйста.")
        bot_info_city(message)
