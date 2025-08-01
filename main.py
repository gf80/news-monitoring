import asyncio
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from bot.telegram_bot import dp, bot, check_and_notify
from parsers.city_news_parser import CityParser
from storage.database import init_db
from config import CHECK_INTERVAL_MINUTES

async def run_scheduler():
    scheduler = AsyncIOScheduler()

    # Парсер каждые N минут
    scheduler.add_job(func=CityParser().fetch_news, trigger="interval", minutes=CHECK_INTERVAL_MINUTES)

    # Отправка уведомлений каждые N минут
    scheduler.add_job(func=check_and_notify, trigger="interval", minutes=CHECK_INTERVAL_MINUTES)

    scheduler.start()

async def main():
    init_db()
    await asyncio.gather(
        run_scheduler(),
        dp.start_polling(bot)
    )

if __name__ == "__main__":
    asyncio.run(main())