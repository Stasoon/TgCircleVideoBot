from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from src.utils import shop_callback


top_up_balance_markup = InlineKeyboardMarkup().insert(InlineKeyboardButton(text='💵 Пополнить баланс 💵', callback_data='top_up_balance'))


def get_shop_markup():
    buttons = [
        InlineKeyboardButton(text='3 шт. за 15 ₽', callback_data=shop_callback.new(count=3, price=15)),
        InlineKeyboardButton(text='10 шт. за 35 ₽', callback_data=shop_callback.new(count=10, price=35)),
        InlineKeyboardButton(text='25 шт. за 50 ₽', callback_data=shop_callback.new(count=25, price=50)),
        InlineKeyboardButton(text='50 шт. за 70 ₽', callback_data=shop_callback.new(count=50, price=70)),
    ]

    markup = InlineKeyboardMarkup(row_width=1)
    for bttn in buttons:
        markup.insert(bttn)
    return markup




