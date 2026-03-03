from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database.database import get_db
from models.author import Author
from schemas.author import AuthorCreate, AuthorResponse

router = APIRouter(prefix="/authors", tags=["authors"])

@router.get("/", response_model=List[AuthorResponse])
def get_authors(db: Session = Depends(get_db)):
    return db.query(Author).all()

@router.get("/{author_id}", response_model=AuthorResponse)
def get_author(author_id: int, db: Session = Depends(get_db)):
    author = db.query(Author).filter(Author.id == author_id).first()
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")
    return author

@router.post("/", response_model=AuthorResponse, status_code=201)
def create_author(author: AuthorCreate, db: Session = Depends(get_db)):
    db_author = Author(**author.model_dump())
    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    return db_author

@router.put("/{author_id}", response_model=AuthorResponse)
def update_author(author_id: int, author: AuthorCreate, db: Session = Depends(get_db)):
    db_author = db.query(Author).filter(Author.id == author_id).first()
    if not db_author:
        raise HTTPException(status_code=404, detail="Author not found")
    
    for key, value in author.model_dump().items():
        setattr(db_author, key, value)
    
    db.commit()
    db.refresh(db_author)
    return db_author

@router.delete("/{author_id}", status_code=204)
def delete_author(author_id: int, db: Session = Depends(get_db)):
    db_author = db.query(Author).filter(Author.id == author_id).first()
    if not db_author:
        raise HTTPException(status_code=404, detail="Author not found")
    
    db.delete(db_author)
    db.commit()
    return None
