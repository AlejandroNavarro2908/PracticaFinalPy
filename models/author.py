from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import relationship
from database.database import Base

class Author(Base):
    __tablename__ = "authors"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    bio = Column(String, nullable=True)
    birth_date = Column(Date, nullable=True)
    nationality = Column(String, nullable=True)

    books = relationship("Book", back_populates="author", cascade="all, delete-orphan")
