from pydantic import BaseModel
from typing import Optional

class BookBase(BaseModel):
    title: str
    summary: Optional[str] = None
    publication_year: Optional[int] = None
    price: float
    author_id: int

class BookCreate(BookBase):
    pass

class BookResponse(BookBase):
    id: int

    class Config:
        from_attributes = True
