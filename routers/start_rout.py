from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from keyboard.keyboard import one_key_kb, main_kb
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup


class MainState(StatesGroup):
    main_menu = State()
    parsing_state = State()

start_router = Router()

@start_router.message(CommandStart())
async def star_cmd(message: Message, state: FSMContext):
    await message.answer('Выбери, что надо и нажми кнопку', reply_markup=main_kb())
    await state.set_state(MainState.main_menu)

@start_router.message(F.text == '🔍 Парсинг', MainState.main_menu)
async def parsing(message: Message, state: FSMContext):
    search_text = 'python'
    await message.answer(f'Я буду отправлять по 10 вакансий по запросу {search_text}. Для продолжения нажмите кнопку ниже', reply_markup=one_key_kb('Продолжить'))
    await state.set_state(MainState.parsing_state)
