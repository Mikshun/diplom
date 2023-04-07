from telebot.types import Message

from keyboards.reply.yas_no import yas_no_button
from loader import bot
from states.need_photo import UserInfoState

no_info = "Нет данных"


def text_example(rest_info: dict) -> str:
    bot_message = "Название ресторана: {name_value}\n" \
                  "Улица: {street}\n" \
                  "Ценовой диапозон: {pricerange} евро\n" \
                  "Рейтинг ресторана: {ratingvalue}\n" \
                  "Количество отзывов: {reviewcount}".format(
                    name_value=rest_info.get("name", no_info),
                    street=rest_info.get("address", no_info).get("street", no_info),
                    pricerange=rest_info.get("priceRange", no_info) if rest_info.get("priceRange", no_info) != 0 else no_info,
                    ratingvalue=rest_info.get("aggregateRatings", no_info).get("thefork", no_info).get("ratingValue",
                                                                                                       no_info) if rest_info.get(
                        "aggregateRatings", no_info).get("thefork", no_info).get("ratingValue", no_info) != 0 else no_info,
                    reviewcount=rest_info.get("aggregateRatings", no_info).get("thefork", no_info).get("reviewCount",
                                                                                                       no_info) if rest_info.get(
                        "aggregateRatings", no_info).get("thefork", no_info).get("reviewCount", no_info) != 0 else no_info
                         )
    return bot_message


def bot_quest(message: Message, response: tuple) -> None:
    bot.set_state(message.from_user.id, UserInfoState.need_photo)
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['response'] = response
    bot.send_message(message.from_user.id, "Вам нужны фото да/нет?", reply_markup=yas_no_button())


@bot.message_handler(state=UserInfoState.need_photo)
def bot_sender(message: Message) -> None:
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        if message.text.lower() == "да":
            for i in data.get('response'):
                if type(i.get("mainPhoto")) == dict and len(i.get("mainPhoto")) > 0:
                    for photo in i["mainPhoto"]:
                        try:
                            bot.send_photo(message.from_user.id, i["mainPhoto"][photo], caption=text_example(i))
                            break
                        except:
                            bot.send_message(message.from_user.id, "Не удалось загрузить фото, загружаю другое")
        elif message.text.lower() == "нет":
            for i in data['response']:
                bot.send_message(message.from_user.id, text_example(i))
        else:
            bot.send_message(message.from_user.id, "Неверный ответ")
    bot.set_state(message.from_user.id, state=None)
