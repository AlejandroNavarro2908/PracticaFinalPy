from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database.database import get_db
from models.book import Book
from models.author import Author
from schemas.book import BookCreate, BookResponse

router = APIRouter(prefix="/books", tags=["books"])

@router.get("/", response_model=List[BookResponse])
def get_books(db: Session = Depends(get_db)):
    return db.query(Book).all()

@router.get("/{book_id}", response_model=BookResponse)
def get_book(book_id: int, db: Session = Depends(get_db)):
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

@router.post("/", response_model=BookResponse, status_code=201)
def create_book(book: BookCreate, db: Session = Depends(get_db)):
    # Check if author exists
    author = db.query(Author).filter(Author.id == book.author_id).first()
    if not author:
        raise HTTPException(status_code=400, detail="Author not found")
        
    db_book = Book(**book.model_dump())
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book

@router.put("/{book_id}", response_model=BookResponse)
def update_book(book_id: int, book: BookCreate, db: Session = Depends(get_db)):
    db_book = db.query(Book).filter(Book.id == book_id).first()
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")
    
    # Check if author exists
    author = db.query(Author).filter(Author.id == book.author_id).first()
    if not author:
        raise HTTPException(status_code=400, detail="Author not found")

    for key, value in book.model_dump().items():
        setattr(db_book, key, value)
    
    db.commit()
    db.refresh(db_book)
    return db_book

@router.delete("/{book_id}", status_code=204)
def delete_book(book_id: int, db: Session = Depends(get_db)):
    db_book = db.query(Book).filter(Book.id == book_id).first()
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")
    
    db.delete(db_book)
    db.commit()
    return None
