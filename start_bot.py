import logging, asyncio, os

from aiogram import Bot, Dispatcher
from dotenv import load_dotenv
from routers.start_rout import start_router
from routers.pars_rout import pars_router
from routers.rss_rout import rss_router
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from config import connection_database




load_dotenv()
async def get_db_connection():
    return connection_database(os.getenv('DATABASE_PASSWORD'))

bot = Bot(token=os.getenv('BOT_TOKEN'), default=DefaultBotProperties(parse_mode=ParseMode.HTML))   #токен из переменной окружения
dp = Dispatcher(data={'conn': get_db_connection}) #Здесь теперь передаётся функция



async def main():
    dp.include_router(start_router)
    dp.include_router(pars_router)
    dp.include_router(rss_router)
    await dp.start_polling(bot)

if __name__ == "__main__": 
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.info('Бот остановлен')

    
