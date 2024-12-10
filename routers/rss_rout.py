from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from keyboard.keyboard import one_key_kb, main_kb
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from rss.rss import connection_database, check_tgid, add_user
from routers.start_rout import MainState
import os


rss_router = Router()

conn = connection_database('Ibra0550-')

@rss_router.message(F.text == 'Начать пересылку', MainState.rss_state)
async def rss_message(message: Message, state: FSMContext):
    await message.answer('Начинаю')
    check = check_tgid(conn=conn, tg_id=message.from_user.id)
    if check is None:
        await message.answer('Вы не подписывались на рассылку. Чтобы подписаться, нажмите на специальную кнопку', reply_markup=one_key_kb('Начать пользоваться рассылкой'))
    await message.answer('Подписка работает')

@rss_router.message(F.text == 'Начать пользоваться рассылкой', MainState.rss_state)
async def start_rss(message: Message, state: FSMContext):
    add_user(conn=conn, tg_id=message.from_user.id)
    await message.answer("Вы добавлены в систему, осталось выбрать источники рассылки: ")
