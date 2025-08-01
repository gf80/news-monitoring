import hashlib


def make_news_hash(title: str, link: str) -> str:
    return hashlib.md5(f"{title}{link}".encode("utf-8")).hexdigest()