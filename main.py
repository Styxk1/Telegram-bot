import asyncio

from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from config import BOT_TOKEN
from apscheduler.schedulers.asyncio import AsyncIOScheduler


loop = asyncio.get_event_loop()
bot = Bot(BOT_TOKEN, parse_mode="HTML")
storage = MemoryStorage()
dp = Dispatcher(bot, loop=loop, storage=storage)
scheduler = AsyncIOScheduler()

if __name__ == "__main__":
    from handlers import dp, send_to_adm_su, send_to_adm_sd, check_time
    scheduler.add_job(check_time, "interval", minute=1, args=(dp,))
    scheduler.start()
    executor.start_polling(dp, on_startup=send_to_adm_su, on_shutdown=send_to_adm_sd)