from aiogram import types, Dispatcher
from src.utils import mailing
from src.create_bot import bot
from src.filters.is_owner import IsOwnerFilter
from src.database import increase_balance_by_value, reset_user_balance, get_user_ids_to_mailing


''' 
    Админские команды:
    /superbalance - увеличивает баланс на 50
    /resetbalance - обнуляет баланс
    
'''

__mailing_text = 'Привет!'
__mailing_link = ''


async def __handle_super_balance_command(message: types.Message):
    increase_balance_by_value(telegram_id=message.from_id, value=50)
    await message.answer('Ваш баланс пополнен на 50.')


async def __handle_reset_balance_command(message: types.Message):
    reset_user_balance(telegram_id=message.from_id)
    await message.answer('Ваш баланс обнулён.')


def __set_mailing_text(message: types.Message):
    user_ids = get_user_ids_to_mailing()
    mailing.mailing_to_users(bot, user_ids, __mailing_text)

#
# def set_mailing_photo(message: types.Message):
#
#
# def set_mailing_button(message: types.Message)


def register_admin_handlers(dp: Dispatcher):
    dp.register_message_handler(__handle_super_balance_command, commands=['superbalance'], is_owner=True)
    dp.register_message_handler(__handle_reset_balance_command, commands=['resetbalance'], is_owner=True)
