from src.config import max_video_size_mb, max_video_duration_sec, max_sides_len_px


def get_start_text(first_name: str = 'пользователь'):
    return f'<b>Привет, {first_name}!</b> \n' + \
            '📎 Я могу конвертировать твоё квадратное Видео в круглое Видеосообщение, просто отправь мне медиафайл. \n\n' + \
            'Если у тебя есть вопросы, Используй команду /help.'


__help_link = "https://tproger.ru/articles/what-junior-python-dev-should-know/"
help_message = f'🔎 <a href="{__help_link}">Статья с объяснением</a> 🔍'


def get_convertation_error_or_none(duration, size, x, y) -> None | str:
    is_ok = True
    err_text = 'К сожалению, Я не могу сконвертировать это видео. Пожалуйста, используй видеоредактор чтобы' \
               ' исправить проблемы ниже: \n\n'

    # проверка продолжительности
    if duration <= max_video_duration_sec:
        err_text += f'✅ Видео не дольше {max_video_duration_sec} секунд. \n'
    else:
        is_ok = False
        err_text += f'⛔ Максимальная продолжительность видео - {max_video_duration_sec} секунд. Ваше видео длится <b>{duration}</b> с. \n'

    # проверка размера (байты)
    if size <= 8*2**20: err_text += f'✅ Видео меньше, чем {max_video_size_mb} Мб. \n'
    else:
        is_ok = False
        err_text += f'⛔ Видео больше {max_video_size_mb} Мб. Размер вашего видео - <b>{size / 2 ** 20 : .2f}</b> Мб \n'

    # проверка отношения сторон
    if x == y: err_text += '✅ Видео имеет отношение сторон 1:1. \n'
    else:
        is_ok = False
        err_text += '⛔ Видео не квадратное, ширина и высота должна быть одинаковы (отношение сторон 1:1). ' + \
                    f'Размеры вашего видео - <b>{x}x{y}</b> (ШxВ) \n'

    # проверка на размеры сторон
    if x <= max_sides_len_px and y <= max_sides_len_px:
        err_text += f'✅ Ширина или высота видео не больше, чем {max_sides_len_px} пикселей. \n'
    else:
        is_ok = False
        err_text += f'⛔ Ширина или высота видео больше чем {max_sides_len_px}. Размеры вашего видео - <b>{x}x{y}</b> (ШxВ) \n'

    return None if is_ok else err_text


want_buy_text = 'Если хотите убрать водяной знак, поддержите проект:'


def get_user_balance_text(balance: int):
    return f'Ваш баланс: <b>{balance} конвертаций</b> без водяного знака.'


# def get_item_description(count: int, price: int) -> str:
#     return f'🥇 <b>Премиум доступ</b> 🥇 \nВы получите <b>{count}</b> Премиум конвертаций без водяного знака за {price} ₽. \n' + \
#             'Используйте ссылку или кнопку ниже. \nДоступ сразу после оплаты.'


unexpected_text = 'Я вас не понимаю. Отправьте мне видео или пропишите /help, если вы не понимаете, как пользоваться ботом.'
