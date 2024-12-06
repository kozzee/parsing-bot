from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from keyboard.start_kb import one_key_kb

start_router = Router()

@start_router.message(CommandStart())
async def star_cmd(message: Message):
    await message.answer('Выбери, что надо и нажми кнопку', reply_markup=one_key_kb('🔍 Парсинг'))