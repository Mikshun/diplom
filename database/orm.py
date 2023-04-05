import json
from .models import *

def create_table():
    with db:
        db.create_tables([User])

def record(message):
    with db:
        User.create(user_id=message.chat.id,request_date=datetime.datetime.now(),request_time=datetime.datetime.now().replace(microsecond=0),result=message)