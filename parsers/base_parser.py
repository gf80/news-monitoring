from abc import ABC, abstractmethod

class BaseParser(ABC):
    @abstractmethod
    async def fetch_news(self):
        """Возвращает список новостей в формате [{'title': ..., 'link': ..., 'date': ...}, ...]"""
        pass
