from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
from keyboard.keyboard import one_key_kb, main_kb, source_kb
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from rss.rss import connection_database, check_tgid, add_user, get_from_database, add_data
from routers.start_rout import MainState
import os

class RssState(StatesGroup):
    nosubscibing = State()


rss_router = Router()

conn = connection_database(os.getenv('DATABASE_PASSWORD'))


@rss_router.message(F.text == 'Начать пересылку', MainState.rss_state)
async def rss_message(message: Message, state: FSMContext):
    await message.answer('Начинаю')
    check = check_tgid(conn=conn, tg_id=message.from_user.id)
    if check is None:
        await state.set_state(RssState.nosubscibing)
        await message.answer('Вы не подписывались на рассылку. Чтобы подписаться, нажмите на специальную кнопку', reply_markup=one_key_kb('Подписаться'))
        return
    await message.answer('Подписка работает')

@rss_router.message(F.text == 'Подписаться', RssState.nosubscibing)
async def start_rss(message: Message, state: FSMContext):
    chek = add_user(conn=conn, tg_id=message.from_user.id)
    if chek:
        await state.set_state(MainState.rss_state)
        await add_rss(message, state)




@rss_router.message(F.text == 'Добавить источник', MainState.rss_state)
async def add_rss(message: Message, state: FSMContext):
    sources = get_from_database(conn=conn, data=['`name`'], table='sources')  
    text = ""
    for i, source in enumerate(sources, start=1):
        name = source[0]  # Получаем значение 'name' из кортежа
        text += f"{i}. {name}\n"
    await message.answer(f"Вот список доступнЫх новостных источников:", reply_markup=source_kb(source=sources))
    print(text)




@rss_router.callback_query(F.data.startswith('addsource_'))
async def add_source(call: CallbackQuery):
    name_source = call.data.replace('addsource_', '')
    print(name_source)
    source_id = get_from_database(conn=conn, data=['source_id'], table='sources', condition='`name` = %s', params=(name_source,))[0][0]
    print(source_id)

    tg_id = call.from_user.id
    user_id = get_from_database(conn=conn, data=['user_id'], table='users', condition='tg_id = %s', params=(tg_id,))[0][0]
    print(user_id)
    chek = add_data(conn=conn, columns=['user_id', 'source_id'], table='subscriptions', values=(user_id, source_id))
    if chek:
        await call.answer(f'Вы подписались на {name_source}')
    else:
        await call.answer('Произошла ошибка при подписке')

    
