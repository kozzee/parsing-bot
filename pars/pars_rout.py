from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from pars.api_hh import extract_vacancies, get_number_of_vacation
from keyboard.start_kb import one_key_kb
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State

pars_router = Router()

@pars_router.message(F.text == '🔍 Парсинг')
async def pars(message : Message):
    await message.answer('Начинаем парсить вакансии!')
    await message.answer('🔎')

    number_vac = get_number_of_vacation()
    await message.answer(f'Найдено {number_vac} вакансий. Показать с первой страницы?', reply_markup=one_key_kb('Покажи'))

@pars_router.message(F.text == 'Покажи')
async def vacant_show(message: Message):
    vacancies = extract_vacancies(page= )
    for i in vacancies:
        answer = f"{i['title']}\n{i['employer']}\n{i['description']}\n{i['link']}"
        await message.answer(answer, reply_markup=one_key_kb('Покажи еще'))

@pars_router.message(F.text == "Покажи еще")
async def next_page(message: Message):
    await vacant_show(message)

    
