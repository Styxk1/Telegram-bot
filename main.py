import asyncio

from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from config import BOT_TOKEN

loop = asyncio.get_event_loop()
bot = Bot(BOT_TOKEN, parse_mode="HTML")
storage = MemoryStorage()
dp = Dispatcher(bot, loop=loop, storage=storage)

if __name__ == "__main__":
    from handlers import dp, send_to_adm_su, send_to_adm_sd
    executor.start_polling(dp, on_startup=send_to_adm_su, on_shutdown=send_to_adm_sd)