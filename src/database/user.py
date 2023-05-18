from .models import User


# region SQL Get

def get_user_by_telegram_id_or_none(telegram_id: int) -> User | None:
    return User.get_or_none(User.telegram_id == telegram_id)


def get_user_balance(telegram_id: int) -> int:
    user = User.get(User.telegram_id == telegram_id)
    return user.balance


def get_user_ids_to_mailing() -> tuple:
    return tuple(user.telegram_id for user in User.select(User.bot_blocked is False))

# endregion


# region SQL Create

def create_user(telegram_id: int, name: str) -> None:
    if not get_user_by_telegram_id_or_none(telegram_id):
        User.create(name=name, telegram_id=telegram_id)
    else:
        switch_bot_blocked_by_user(telegram_id)


# endregion


# region SQL Update

def increase_balance_by_value(telegram_id: int, value: int) -> None:
    user = User.get(User.telegram_id == telegram_id)
    user.balance += value
    user.save()


def reduce_balance_by_one(telegram_id: int) -> None:
    user = User.get(User.telegram_id == telegram_id)
    user.balance -= 1
    user.save()


def reset_user_balance(telegram_id: int) -> None:
    user = User.get(User.telegram_id == telegram_id)
    user.balance = 0
    user.save()


def switch_bot_blocked_by_user(telegram_id: int) -> None:
    user = User.get(User.telegram_id == telegram_id)
    user.bot_blocked = not user.bot_blocked
    user.save()

# endregion
