import logging, asyncio, os

from aiogram import Bot, Dispatcher
from dotenv import load_dotenv
from routers.start_rout import start_router
from routers.pars_rout import pars_router
from routers.rss_rout import rss_router
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode


load_dotenv()


bot = Bot(token=os.getenv('BOT_TOKEN'), default=DefaultBotProperties(parse_mode=ParseMode.HTML))   #токен из переменной окружения
dp = Dispatcher()



async def main():
    dp.include_router(start_router)
    dp.include_router(pars_router)
    dp.include_router(rss_router)
    await dp.start_polling(bot)

if __name__ == "__main__": 
    asyncio.run(main())
