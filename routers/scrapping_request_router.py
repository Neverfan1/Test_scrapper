import datetime
from typing import List

from fastapi import APIRouter, Depends

from schemas.scraping_request import *
from service.scraping_request_service import ScrapingRequestService

router = APIRouter(prefix="/scrap", tags=["ScrapingRequest"])


@router.post("/", response_model=StartScrap)
async def start_scrap(
        list_url: ListURl,
        service: ScrapingRequestService = Depends(),
):
    """Запуск скрапинга"""
    return service.create_scraping_request(list_url)


@router.get("/status/", response_model=StatusScraping)
async def status_scrap(
        scrap_id: int,
        service: ScrapingRequestService = Depends(),
):
    """Получение статуса скрапа"""
    return service.get_scraping_status(scrap_id)


@router.get("/html/", response_model=HtmlScraping)
async def html_scrap(
        scrap_id: int,
        service: ScrapingRequestService = Depends(),
):
    """Получение html скрапа"""
    return service.get_scraping_html(scrap_id)
