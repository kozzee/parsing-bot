import logging, asyncio, os

from aiogram import Bot, Dispatcher
from dotenv import load_dotenv
from routers.start_rout import start_router
from routers.pars_rout import pars_router
from routers.rss_rout import rss_router


load_dotenv()


bot = Bot('7400809027:AAHnVFYCaVIqt5ILml2ZGfc5dWUTRL73VMU')   #токен из переменной окружения
dp = Dispatcher()

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s') #шаблон для работы логгирования
logger = logging.getLogger(__name__)

async def main():
    dp.include_router(start_router)
    dp.include_router(pars_router)
    dp.include_router(rss_router)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
