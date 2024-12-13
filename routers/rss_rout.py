from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery
from keyboard.keyboard import one_key_kb, main_kb, source_kb, change_rss_kb
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from rss.rss import check_tgid, add_user, get_from_database, add_data, check_data, parsing_url, get_url_from_database, get_and_send_news
from routers.start_rout import MainState
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from config import logger

import os



rss_router = Router()



# scheduler = AsyncIOScheduler()  

class RssState(StatesGroup):
    nosubscibing = State() #состояние если пользователя нет в базе данных






@rss_router.message(F.text == 'Начать пересылку', MainState.rss_state) #запускает планировщик
async def rss_message(message: Message, state: FSMContext, bot: Bot, data: dict):
    tg_id = message.from_user.id
    conn = await data['conn']()
    check = check_tgid(conn=conn, tg_id=tg_id)
    
    if check is None:
        await state.set_state(RssState.nosubscibing)
        await message.answer('Вы не подписывались на рассылку. Чтобы подписаться, нажмите на специальную кнопку', reply_markup=one_key_kb('Подписаться'))
        return
    if 'schedulers' not in data:
        data['schedulers'] = {}
    if tg_id not in data['schedulers']:
        data['schedulers'][tg_id] = AsyncIOScheduler() #Создаём планировщик для каждого пользователя
        data['schedulers'][tg_id].start() #Запускаем планировщик для каждого пользователя
    data['schedulers'][tg_id].add_job(send_news_periodically, "interval", minutes=1,
                                      args=(tg_id, bot), kwargs={'data': data})
 
    await message.answer('Ждите новых новостей')



@rss_router.message(F.text == 'Подписаться', RssState.nosubscibing)
async def start_rss(message: Message, state: FSMContext, data: dict):
    conn = await data['conn']()
    chek = add_user(conn=conn, tg_id=message.from_user.id) #добавляет нового пользователя в базу
    if chek:
        await state.set_state(MainState.rss_state)
        await add_rss(message, state)




@rss_router.message(F.text == 'Добавить источник', MainState.rss_state)   #кнопка выводит источники для подписки
async def add_rss(message: Message, state: FSMContext, data: dict):
    conn = await data['conn']()
    sources = get_from_database(conn=conn, data=['`name`'], table='sources')  
    await message.answer(f"Вот список доступнЫх новостных источников:", reply_markup=source_kb(source=sources))



@rss_router.callback_query(F.data.startswith('addsource_'))  #Обработка подписки на источник
async def add_source(call: CallbackQuery, data: dict):
    conn = await data['conn']()
    name_source = call.data.replace('addsource_', '')
    source_data = get_from_database(conn=conn, data=['source_id'], table='sources', condition='`name` = %s', params=(name_source,))
    if not source_data:
        await call.answer('Источник не найден')
        return

    source_id = source_data[0][0]
    tg_id = call.from_user.id

    user_data = get_from_database(conn=conn, data=['user_id'], table='users', condition='tg_id = %s', params=(tg_id,))
    if not user_data:
        await call.answer('Пользователь не найден')
        return

    user_id = user_data[0][0]
    print(user_id)

    if check_data(conn=conn, table='subscriptions', first_value_column='user_id',
        second_value_column='source_id', first_value=user_id, second_value=source_id):
        await call.answer('Вы уже подписаны на этот источник')
        return  # Останавливаем выполнение, если связь существует


    if not add_data(conn=conn, columns=['user_id', 'source_id'], table='subscriptions', values=(user_id, source_id)):
        await call.answer('Произошла ошибка при подписке')
    else:
        await call.answer(f'Вы подписались на {name_source}')


@rss_router.message(F.text == 'Показать последние новости', MainState.rss_state)
async def show_news(message: Message, state: FSMContext, data: dict):
    conn = await data['conn']()
    user_id_data = get_from_database(conn, ['user_id'], 'users', 'tg_id = %s', (message.from_user.id,))
    if not user_id_data:
        await message.answer('Пользователь не найден')
        return
    user_id = user_id_data[0][0]

    list_source = get_from_database(conn, ['source_id'], 'subscriptions', 'user_id = %s', (user_id,))
    if not list_source:
        await message.answer('Вы не подписаны ни на один источник')
        return

    list_url = [get_url_from_database(conn, i[0]) for i in list_source if get_url_from_database(conn, i[0])]
    news_list = parsing_url(list_url)

    for title, description, link in news_list:
        if not check_data(conn, 'news', 'user_id', 'link', user_id, link):
            await message.answer(f"<b>{title}</b>\n\n{description}\n\nСсылка: {link}")

            # Используем get_from_database для получения source_id по URL
            source_id_data = get_from_database(conn, ['source_id'], 'sources', 'url = %s', (list_url[0],))  # Передаем URL из list_url
            if source_id_data:
                source_id = source_id_data[0][0]
                add_data(conn, 'news', ['source_id', 'title', 'description', 'link', 'user_id'], (source_id, title, description, link, user_id))
            else:
                logger.error(f"Не удалось найти source_id для URL: {list_url[0]}")  # Логируем ошибку, если source_id не найден



@rss_router.message(F.text == 'Управление источниками', MainState.rss_state)
async def change_rss(message: Message, state: FSMContext):
    await message.answer("Здесь вы можете управлять своими новостными источниками", reply_markup=change_rss_kb())


async def exit_rss(message: Message, state: FSMContext, data: dict): # Добавлено data
    tg_id = message.from_user.id
    if tg_id in data['schedulers']:
        data['schedulers'][tg_id].shutdown()
        del data['schedulers'][tg_id] # Удаляем планировщик после остановки
    await state.set_state(MainState.main_menu)
    await message.answer('Отправка сообщений остановлена', reply_markup=main_kb())

async def send_news_periodically(user_id: int, bot: Bot, data: dict):
    conn = await data['conn']()
    """Функция для отправки новостей по расписанию."""
    try:
        # Получение объекта бота из диспетчера
 

        user_id_data = get_from_database(conn, ['user_id'], 'users', 'tg_id = %s', (user_id,))
        if not user_id_data:
            logger.error(f"Пользователь с tg_id {user_id} не найден в базе данных.")
            return  # Прекращаем выполнение, если пользователь не найден

        user_id_db = user_id_data[0][0]  # user_id из базы данных

        list_source = get_from_database(conn, ['source_id'], 'subscriptions', 'user_id = %s', (user_id_db,))
        if not list_source:
            logger.info(f"Пользователь {user_id} не подписан ни на один источник.")
            return  # Прекращаем выполнение, если нет подписок

        list_url = [get_url_from_database(conn, i[0]) for i in list_source if get_url_from_database(conn, i[0])]
        if not list_url:
            logger.error(f"Не удалось получить URL для источников пользователя {user_id}.")
            return

        news_list = parsing_url(list_url)
        if not news_list:
            logger.info(f"Нет новых новостей для пользователя {user_id}.")
            return

        for title, description, link in news_list:
            if not check_data(conn, 'news', 'user_id', 'link', user_id_db, link):
                try:
                    await bot.send_message(chat_id=user_id, text=f"<b>{title}</b>\n\n{description}\n\nСсылка: {link}", parse_mode="HTML")
                    source_id_data = get_from_database(conn, ['source_id'], 'sources', 'url = %s', (list_url[0],))
                    if source_id_data:
                        source_id = source_id_data[0][0]
                        add_data(conn, 'news', ['source_id', 'title', 'description', 'link', 'user_id'], (source_id, title, description, link, user_id_db))
                    else:
                        logger.error(f"Не удалось найти source_id для URL: {list_url[0]}") 

                except Exception as e:
                    logger.exception(f"Ошибка при отправке сообщения пользователю {user_id}: {e}")

    except Exception as e:
        logger.exception(f"Ошибка в функции send_news_periodically: {e}")





