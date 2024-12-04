from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from keyboard.start_kb import main_kb

start_router = Router()

@start_router.message(CommandStart())
async def star_cmd(message: Message):
    await message.answer('Мы начнем парсировать вакансии на HH.ru. Ниже Кнопки для дальнейшей работы:', reply_markup=main_kb())