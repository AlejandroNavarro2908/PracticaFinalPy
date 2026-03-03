from pydantic import BaseModel
from datetime import date
from typing import Optional, List

class AuthorBase(BaseModel):
    name: str
    bio: Optional[str] = None
    birth_date: Optional[date] = None
    nationality: Optional[str] = None

class AuthorCreate(AuthorBase):
    pass

class AuthorResponse(AuthorBase):
    id: int

    class Config:
        from_attributes = True
