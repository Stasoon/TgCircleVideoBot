from aiogram import types, Dispatcher
from aiogram.types.message import ContentType

from src.keyboards.user import get_shop_markup, top_up_balance_markup
from src.utils import messages, send_video_as_note, shop_callback
from src.create_bot import bot
from src.database import create_user, get_user_balance, increase_balance_by_value, reduce_balance_by_one
from src.config import PAYMASTER_TOKEN


async def __handle_start_command(message: types.Message) -> None:
    create_user(message.from_id, message.from_user.first_name)
    await message.answer(messages.get_start_text(message.from_user.first_name))


async def __handle_help_command(message: types.Message) -> None:
    await message.answer(messages.help_message)


async def __handle_balance_command(message: types.Message) -> None:
    balance = get_user_balance(message.from_id)
    await message.answer(messages.get_user_balance_text(balance), reply_markup=top_up_balance_markup)


async def __handle_video(message: types.Message) -> None:
    user_video = message.video
    convert_error = messages.get_convertation_error_or_none(user_video.duration, user_video.file_size, user_video.width, user_video.height)

    # если есть ошибка, отправляем её
    if not user_video or convert_error is not None:
        await message.reply(convert_error)
        return

    if get_user_balance(message.from_id) < 1:
        note_message = await send_video_as_note(message, add_watermark=True)
        await note_message.reply(messages.want_buy_text, reply_markup=top_up_balance_markup)
    else:
        await send_video_as_note(message, add_watermark=False)
        reduce_balance_by_one(telegram_id=message.from_id)
        await __handle_balance_command(message)


async def __handle_top_up_balance_callback(callback: types.CallbackQuery) -> None:
    await callback.message.answer(messages.want_buy_text, reply_markup=get_shop_markup())
    await callback.answer()


async def __handle_shop_item_callback(callback: types.CallbackQuery, callback_data: dict) -> None:
    PRICES = [
        types.LabeledPrice(label=f"Покупка {callback_data.get('count')}", amount=int(callback_data.get('price'))*100),
    ]
    await bot.send_invoice(
        chat_id=callback.from_user.id,
        title='🥇 Премиум доступ 🥇',
        description=f"Покупка {callback_data.get('count')} конвертаций без водяного знака. \nДоступ получите сразу после покупки",
        provider_token=PAYMASTER_TOKEN,
        currency='rub',
        payload=f"{callback_data.get('count')}",
        start_parameter=56,
        prices=PRICES,
    )

    # await callback.message.answer(messages.get_item_description(callback_data.get('count'), callback_data.get('price')))
    await callback.answer()
    await callback.message.delete()


async def __handle_pre_checkout_query(pre_check_q: types.PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_check_q.id, ok=True)


async def __succesfull_payment(message: types.Message):
    increase_balance_by_value(message.from_id, int(message.successful_payment.to_python().get('invoice_payload')))
    await message.answer('Баланс пополнен! Чтобы просмотреть, /balance')


async def __handle_unexpected_messages(message: types.Message) -> None:
    await message.answer(messages.unexpected_text)


def register_user_handlers(dp: Dispatcher) -> None:
    # Обработка фото
    dp.register_message_handler(__handle_start_command, commands=['start'])
    dp.register_message_handler(__handle_help_command, commands=['help'])
    dp.register_message_handler(__handle_balance_command, commands=['balance'])
    dp.register_message_handler(__handle_video, content_types=['video'])

    # Платежи
    dp.register_callback_query_handler(__handle_top_up_balance_callback, text='top_up_balance')
    dp.register_callback_query_handler(__handle_shop_item_callback, shop_callback.filter())
    dp.register_pre_checkout_query_handler(__handle_pre_checkout_query, lambda query: True)
    dp.register_message_handler(__succesfull_payment, content_types=[ContentType.SUCCESSFUL_PAYMENT])

    # Непредусмотренные сообщения
    dp.register_message_handler(__handle_unexpected_messages, content_types=['text', 'video-note', 'photo'])
