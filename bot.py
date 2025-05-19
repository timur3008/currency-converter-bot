import os, asyncio

from aiogram import Bot, Dispatcher
from dotenv import load_dotenv

from handlers import routers_list

async def main():
    load_dotenv()
    BOT_TOKEN = os.getenv('BOT_TOKEN')

    bot = Bot(token=BOT_TOKEN)
    dispatcher = Dispatcher()

    dispatcher.include_routers(*routers_list)
    print('[+] BOT WORKING -> STARTED')
    await dispatcher.start_polling(bot)

try:
    asyncio.run(main())
except KeyboardInterrupt:
    print('[-] BOT WORKING -> STOPPED')