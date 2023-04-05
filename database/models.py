from peewee import *

db = SqliteDatabase("database/db/database.db")

class User(Model):
    id=PrimaryKeyField(unique=True)
    user_id=IntegerField()
    request_date = DateField()
    request_time=TimeField()
    result=TextField()

    class Meta:
        database = db
        order_by = 'id'
        db_table='Users'

