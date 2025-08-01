import hashlib


def make_news_hash(title: str, link: str) -> str:
    return hashlib.md5(f"{title}{link}".encode("utf-8")).hexdigest()

from datetime import datetime

MONTHS_RU = {
    "января": 1, "февраля": 2, "марта": 3, "апреля": 4,
    "мая": 5, "июня": 6, "июля": 7, "августа": 8,
    "сентября": 9, "октября": 10, "ноября": 11, "декабря": 12
}

def parse_russian_date(date_str: str) -> str:
    # Пример входа: "1 августа, 15:34"
    parts = date_str.replace(",", "").split()
    day = int(parts[0])
    month = MONTHS_RU[parts[1]]
    time_part = parts[2]

    now = datetime.now()
    dt = datetime.strptime(f"{day}.{month}.{now.year} {time_part}", "%d.%m.%Y %H:%M")
    
    # Возвращаем ISO-формат для БД
    return dt.strftime("%Y-%m-%d %H:%M:%S")