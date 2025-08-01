from bot.telegram_bot import bot
from storage.database import init_db
from config import CHECK_INTERVAL_MINUTES


def start_bot():
    print("[INFO] Telegram бот запущен!")
    bot.polling(none_stop=True)

if __name__ == "__main__":
    # Инициализация БД
    init_db()
    
    # Старт бота
    start_bot()