import requests
from bs4 import BeautifulSoup as bs

from parsers.base_parser import BaseParser

from config import NEWS_URL

from storage.database import add_news


class CityParser(BaseParser):
    URL = NEWS_URL

    def fetch_news(self) -> list[dict]:
        r = requests.get(self.URL)
        soup = bs(r.text, "html.parser")

        news = []
        for item in soup.select("article.posts-search-item"):
            title = item.select_one("h3.posts-search-item-title").get_text(strip=True)
            link = item.select_one("a")["href"]
            date = item.select_one("p.posts-search-item-date").get_text(strip=True)

            new = {
                "title": title,
                "link": link,
                "date": date,
            }

            add_news(title, link, date)
            news.append(new)

        return news