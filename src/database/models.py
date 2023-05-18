from datetime import datetime
from peewee import Model, SqliteDatabase, FloatField, ForeignKeyField, IntegerField, DateTimeField, DateField, BooleanField, TextField


db = SqliteDatabase('database.db')


class _BaseModel(Model):
    class Meta:
        database = db


class User(_BaseModel):
    class Meta:
        db_table = 'Users'

    name = TextField(null=False, default='Пользователь')
    telegram_id = IntegerField(unique=True, null=False)
    registration_date = DateField(default=datetime.today())
    balance = IntegerField(default=0)
    bot_blocked = BooleanField(default=False)


class Payment(_BaseModel):
    class Meta:
        db_table = 'Payments'

    user = ForeignKeyField(User)
    price = FloatField()
    timestamp = DateTimeField(default=datetime.now())


def register_models() -> None:
    for model in _BaseModel.__subclasses__():
        model.create_table()
