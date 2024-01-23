from abc import ABC, abstractmethod


class IScraper(ABC):
    @abstractmethod
    async def fetch():
        ...

    @abstractmethod
    async def scrape_page():
        ...

    @abstractmethod
    async def get_last_page_number():
        ...
