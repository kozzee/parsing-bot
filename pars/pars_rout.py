from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message

pars_router = Router()

@pars_router.message(F.text == '🔍 Парсинг')
async def pars(message : Message):
    await message.answer('Начинаем парсить вакансии')
