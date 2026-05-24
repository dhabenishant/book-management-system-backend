from pydantic import BaseModel, Field


class CreateBookRequest(BaseModel):
    title: str = Field(..., min_length=1)
    author: str = Field(..., min_length=1)
    isbn: str = Field(..., min_length=10)
    category: str = Field(..., min_length=1)
    price: float = Field(..., gt=0)
    published_date: str
    description: str = Field(..., min_length=1)
    cover_image: str
    stock: int = Field(..., ge=0)


class UpdateBookRequest(BaseModel):
    title: str = None
    author: str = None
    isbn: str = None
    category: str = None
    price: float = None
    published_date: str = None
    description: str = None
    cover_image: str = None
    stock: int = None


class BookOut(BaseModel):
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
    created_at: str

    class Config:
        populate_by_name = True
