from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from pars.api_hh import extract_vacancies, get_number_of_vacation
from pars import api_hh

pars_router = Router()

@pars_router.message(F.text == '🔍 Парсинг')
async def pars(message : Message):
    await message.answer('Начинаем парсить вакансии!')
    await message.answer('🔎')

    number_vac = get_number_of_vacation()
    await message.answer(f'Найдено {number_vac} вакансий. Показать с первой страницы?')

@pars_router.message(F.text == 'Покажи')
async def vacant_show(message: Message):
    vacancies = extract_vacancies()
    for i in vacancies:
        answer = f"{i['title']}\n{i['employer']}\n{i['description']}\n{i['link']}"
        await message.answer(answer)

