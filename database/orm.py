import datetime
from database import models
import json


def create_table():
    with models.db:
        models.db.create_tables([models.User])


def record(response: tuple, message_text: str, message_chat_id: int, city: str) -> None:
    with models.db:
        if len(models.User.select().where(models.User.user_id == message_chat_id)) == 5:
            users_list = models.User.select().where(models.User.user_id == message_chat_id).order_by(models.User.id)
            user_first_record = models.User.get(models.User.id == users_list[0])
            user_first_record.delete_instance()

        models.User.create(user_id=message_chat_id, command=message_text, city=city,
                           request_date=datetime.datetime.now(),
                           request_time=datetime.datetime.now().replace(microsecond=0), result=json.dumps(response))
