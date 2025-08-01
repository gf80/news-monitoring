import time
from datetime import datetime
from bot.telegram_bot import check_and_notify
from parsers.city_news_parser import CityParser
from storage.database import add_news, init_db, get_mailings_users, get_unsent_news
from config import CHECK_INTERVAL_MINUTES

class ParserRunner:
    def __init__(self):
        self.parser = CityParser()
        old_news = get_unsent_news()

    def run(self):

        while True:
            try:
                print("[INFO] Запуск парсинга новостей...")
                self.parser.fetch_news()
                
                check_and_notify()

                print(f"[INFO] {datetime.now()} Парсинг завершен. Ожидание {CHECK_INTERVAL_MINUTES} минут...")
                time.sleep(CHECK_INTERVAL_MINUTES * 60)
            
            except Exception as e:
                print(f"[ERROR] Ошибка при парсинге: {e}")
                time.sleep(60)  # Ждем минуту при ошибке

if __name__ == "__main__":
    runner = ParserRunner()
    runner.run()