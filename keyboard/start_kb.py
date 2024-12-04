from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


def main_kb():            #Клавиатура, которая появится первой, после команды /start
    kb = [
        [KeyboardButton(text="🔍 Парсинг")]
        ]
    keyboard = ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        one_time_keyboard=True,
        input_field_placeholder="Давай, выбирай"
    )
    return keyboard