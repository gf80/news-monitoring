from abc import ABC, abstractmethod

class BaseParser(ABC):
    @abstractmethod
    def fetch_news(self) -> list[dict]:
        """Возвращает список новостей в формате [{'title': ..., 'link': ..., 'date': ...}, ...]"""
        pass
