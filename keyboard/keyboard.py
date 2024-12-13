from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton

def main_kb():
    kb = [
        [KeyboardButton(text='🔍 Парсинг')],
        [KeyboardButton(text='📰Новости')]
    ]
    keyboard = ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        one_time_keyboard=True,
        input_field_placeholder='Выбери действие'
    )
    return keyboard

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

def rss_kb():
    kb = [
        [KeyboardButton(text='Начать пересылку')],
        [KeyboardButton(text='Управление источниками')],
        [KeyboardButton(text='Показать последние новости')],
        [KeyboardButton(text='Главное меню')]
        ]
    keyboard = ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        one_time_keyboard=True,
        input_field_placeholder='Выберите команду'
    )
    return keyboard

def source_kb(source: list) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for row in source:
        name_source = row[0]
        builder.row(
            InlineKeyboardButton(
                text=name_source,
                callback_data=f'addsource_{name_source}'
            )
        )
    builder.adjust(1)
    return builder.as_markup()

def change_rss_kb():
    kb = [
        [KeyboardButton(text='Добавить источник')],
        [KeyboardButton(text='Удалить источник')],
        [KeyboardButton(text='Главное меню')]
    ]
    keyboard = ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        one_time_keyboard=True,
        input_field_placeholder='Действие'
    )
    return keyboard
