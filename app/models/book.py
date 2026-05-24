from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class Book(BaseModel):
    id: Optional[str] = Field(None, alias="_id")
    title: str
    author: str
    isbn: str
    category: str
    price: float
    published_date: str
    description: str
    cover_image: str
    stock: int
    created_by: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True


class BookResponse(BaseModel):
    id: str = Field(alias="_id")
    title: str
    author: str
    isbn: str
    category: str
    price: float
    published_date: str
    description: str
    cover_image: str
    stock: int
    created_by: str
    created_at: datetime

    class Config:
        populate_by_name = True


class BooksListResponse(BaseModel):
    data: list[BookResponse]
    total: int
    page: int
    limit: int
    pages: int
