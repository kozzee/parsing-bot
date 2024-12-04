from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message

start_rt = Router()

@start_rt.message(CommandStart())
async def star_cmd(message: Message):
    await message.answer('Мы начнем парсировать вакансии на HH.ru. Ниже Кнопки для дальнейшей работы:')

