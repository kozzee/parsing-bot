from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


def one_key_kb(text, placeholder='Нажми на кнопку'):
    kb = [
        [KeyboardButton(text=text)]
    ]
    keyboard = ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        one_time_keyboard=True,
        input_field_placeholder=placeholder
    )
    return keyboard


def two_key_kb(first_button_text, second_button_text):
    kb = [
        [KeyboardButton(text=first_button_text)],
        [KeyboardButton(text=second_button_text)]
    ]
    keyboard = ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        one_time_keyboard=True,
        input_field_placeholder='Выберите команду'
    )
    return keyboard
