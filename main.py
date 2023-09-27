from aiogram import executor
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from modules.handlers import dp, send_to_adm_su, send_to_adm_sd, check_time


def main():
    scheduler = AsyncIOScheduler()
    scheduler.add_job(check_time, "interval", minutes=1, args=(dp,))
    scheduler.start()
    settings = {"on_startup": send_to_adm_su, "on_shutdown": send_to_adm_sd}
    executor.start_polling(dp, **settings)


if __name__ == "__main__":
    main()
