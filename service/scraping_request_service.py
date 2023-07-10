import asyncio

from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_session
from models.scraping_request_table import ScrapingRequestTable
from schemas.scraping_request import *
import requests


class ScrapingRequestService:

    def __init__(self, session: Session = Depends(get_session)):
        self.session = session

    def _get(self, scrap_id: int) -> ScrapingRequestTable:
        """
        метод получения запроса по id выносим для переиспользования в других методах

        :param scrap_id: идентификатор заказа
        :return: ScrapingRequestTable
        """

        operation = self.session.query(ScrapingRequestTable).filter_by(id=scrap_id).first()

        if not operation:
            raise HTTPException(status_code=404, detail="Запрос с таким идентификатором не найден")

        return operation

    @staticmethod
    def fetch_html(url):
        try:
            response = requests.get(url)
            response.raise_for_status()  # Проверяем статус ответа на ошибки
            return response.text  # Возвращаем HTML-код страницы
        except requests.RequestException as e:
            # Обработка ошибок при сборе HTML
            print(f"Error fetching HTML for URL {url}: {str(e)}")
            return None

    async def scrape_urls(self, scrap_id: int, urls: ListURl):
        operation = self._get(scrap_id)
        for url in urls.urls:
            html = self.fetch_html(url)
            if html is not None:
                # Обновляем данные в базе данных
                if operation.html is None:
                    operation.html = {}
                operation.html[url] = html
        # По завершении скрапинга меняем статус на "готово"
        operation.status = "Готово"
        self.session.commit()

    def create_scraping_request(self, list_url: ListURl) -> StartScrap:

        new_scrap = ScrapingRequestTable(
            urls=list_url.urls,
            status="В процессе",
        )

        self.session.add(new_scrap)
        self.session.commit()

        asyncio.create_task(self.scrape_urls(new_scrap.id, list_url))
        return StartScrap(message="Скрап начался", scrap_id=new_scrap.id)

    def get_scraping_status(self, scrap_id) -> StatusScraping:
        operation = self._get(scrap_id)
        if operation is None:
            raise HTTPException(status_code=404, detail="Запрос с таким идентификатором не найден")
        return StatusScraping(status=operation.status)

    def get_scraping_html(self, scrap_id) -> HtmlScraping:
        operation = self._get(scrap_id)
        if operation is None:
            raise HTTPException(status_code=404, detail="Запрос с таким идентификатором не найден")
        if operation.status != "Готово":
            raise HTTPException(status_code=400, detail="Данные еще не собраны")
        return HtmlScraping(html=operation.html)
