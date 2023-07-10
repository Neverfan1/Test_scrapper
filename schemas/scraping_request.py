from pydantic import BaseModel


class ScrapingRequest(BaseModel):
    id: int
    urls: list[str]
    status: str
    html: dict

    class Config:
        orm_mode = True


class StartScrap(BaseModel):
    message: str
    scrap_id: int


class ListURl(BaseModel):
    urls: list[str]


class StatusScraping(BaseModel):
    status: str


class HtmlScraping(BaseModel):
    html: dict
