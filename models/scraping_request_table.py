from sqlalchemy import (
    Column,
    Integer,
    Text,
)

from sqlalchemy.dialects.postgresql import JSONB
from .base import Base


class ScrapingRequestTable(Base):
    __tablename__ = "scraping_requests"

    id = Column(Integer, primary_key=True)
    urls = Column(Text, nullable=False)
    status = Column(Text, nullable=False)
    html = Column(JSONB)
