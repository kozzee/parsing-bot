from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from pars.api_hh import get_vacancies
from keyboard.start_kb import one_key_kb, two_key_kb
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from heand.start_rout import MainState


pars_router = Router()
    
class ParsingState(StatesGroup):
    page_state = State()



@pars_router.message(F.text == 'Продолжить', MainState.parsing_state)
async def pars(message: Message, state: FSMContext):
    await state.set_state(ParsingState.page_state)
    await state.update_data(page=0)
    await message.answer('Держи вакансии')
    page = 0
    vacancies = get_vacancies(page)
    for i in vacancies:
        answer = f"{i['title']}\n{i['employer']}\n{i['description']}\n{i['link']}"
        await message.answer(answer)
    await message.answer('Показать еще?', reply_markup=two_key_kb('Покажи', 'Главное меню'))

    

@pars_router.message(F.text == 'Покажи', ParsingState.page_state)
async def pars_too(message: Message, state: FSMContext):
    data = await state.get_data()
    page = data['page'] + 1
    await state.update_data(page=page)
    vacancies = get_vacancies(page)
    if vacancies:
        for i in vacancies:
            answer = f"{i['title']}\n{i['employer']}\n{i['description']}\n{i['link']}"
            await message.answer(answer)
    else:
        await message.answer('Вакансий больше нет', reply_markup=one_key_kb('Главное меню'))

@pars_router.message(F.text == 'Главное меню', ParsingState.page_state)
async def exit_pars(message: Message, state: FSMContext):
    await state.set_state(MainState.main_menu)
    await message.answer('Выбирай режим', reply_markup=one_key_kb('Конец круга'))
        
    


# @pars_router.message(F.text == '🔍 Парсинг')
# async def pars(message : Message, state: FSMContext):
#     await state.set_state(VacancyStates.show_vacancies)
#     await state.update_data(page=0)
#     await message.answer('Начинаем парсить вакансии!')
#     await message.answer('🔎')
#     vacancies = get_vacancies()
#     for i in vacancies:
#         answer = f"{i['title']}\n{i['employer']}\n{i['description']}\n{i['link']}"
#         await message.answer(answer, reply_markup=one_key_kb('Покажи еще'))
#     await message.answer('Показать еще?', reply_markup=one_key_kb('Покажи еще'))

# @pars_router.message(F.text == 'Покажи')
# async def vacant_show(message: Message):
#     vacancies = get_vacancies()
#     for i in vacancies:
#         answer = f"{i['title']}\n{i['employer']}\n{i['description']}\n{i['link']}"
#         await message.answer(answer, reply_markup=one_key_kb('Покажи еще'))

@pars_router.message(F.text == 'Покажи еще')
async def next_page(message: Message, state: FSMContext):
    data = await state.get_data()
    page = data['page'] + 1
    await state.update_data(page=page)
    vacancies = get_vacancies(page)
    for i in vacancies:
        answer = f"{i['title']}\n{i['employer']}\n{i['description']}\n{i['link']}"
        await message.answer(answer, reply_markup=one_key_kb('Покажи еще'))

    
