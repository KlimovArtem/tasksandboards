import random


def get_confirm_code() -> str:
    """Функция возврашает строковое представление случайного 4х значного числа."""
    return str(random.randint(1001, 9999))