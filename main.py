import uvicorn
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from routers import router
from settings import settings

tags_metadata = []

app = FastAPI(
    openapi_tags=tags_metadata,
    title="FastApi Microservice of Test Scrapper",
    version="0.0.1",
    description="Microservice of Test Scrapper",
)

app.include_router(router)

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")


app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.server_host,
        port=settings.server_port,
        reload=True,
    )


@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})
