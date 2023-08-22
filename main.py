import asyncio

from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from config.config import BOT_TOKEN

bot = Bot(BOT_TOKEN, parse_mode="HTML")
loop = asyncio.get_event_loop()
storage = MemoryStorage()
dp = Dispatcher(bot, loop=loop, storage=storage)


def main():
    from modules.handlers import dp, send_to_adm_su, send_to_adm_sd, check_time

    scheduler = AsyncIOScheduler()
    scheduler.add_job(check_time, "interval", minutes=1, args=(dp,))
    scheduler.start()
    settings = {"on_startup": send_to_adm_su, "on_shutdown": send_to_adm_sd}
    executor.start_polling(dp, **settings)


if __name__ == "__main__":
    main()
