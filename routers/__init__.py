from fastapi import APIRouter

from . import scrapping_request_router

router = APIRouter()

router.include_router(scrapping_request_router.router)
