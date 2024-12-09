from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from keyboard.keyboard import one_key_kb, main_kb
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from rss.rss import connection_database
from start_rout import MainState
import os


rss_router = Router()

conn = connection_database(os.getenv('DATABASE_PASSWORD'))

@rss_router(F.text == 'Начать пересылку', MainState.rss_state)
async def rss_message(message: Message, state: FSMContext):
    await message.answer('Начинаю')
    
