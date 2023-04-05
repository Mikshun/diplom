import datetime
from database import models


def create_table():
    with models.db:
        models.db.create_tables([models.User])


def record(message, id):
    with models.db:
        models.User.create(user_id=id, request_date=datetime.datetime.now(),
                           request_time=datetime.datetime.now().replace(microsecond=0), result=message)
