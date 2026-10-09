from fastapi import APIRouter, Depends, HTTPException, Path
from Books.models import BookModel
from Books.schemas import *
from sqlalchemy.orm import Session
from core.database import get_db
from typing import List
from fastapi.responses import JSONResponse

router = APIRouter(tags=["personal_library"])

@router.get("/books", response_model=List[BookNameandAuthorResponseSchema])
async def retrieve_the_whole_books(db: Session = Depends(get_db)):
    #only the name of the book and the author will be returned
    result = db.query(BookModel.title_of_the_book, BookModel.author).all()
    return result

@router.get("/books/{book_id}", response_model=BookNameandAuthorResponseSchema)
async def retrieve_the_targeted_book(book_id: int = Path(..., gt = 0), db: Session = Depends(get_db)):
    #only the name of the book and the author will be returned
    result = db.query(BookModel.title_of_the_book, BookModel.author).filter(BookModel.id == book_id).first()
    if not result:
        raise HTTPException(status_code=404, detail="Book not found")
    return result

@router.get("/personal_books", response_model=List[BookResponseSchema])
async def retrieve_the_whole_personal_books(db: Session = Depends(get_db)):
    result = db.query(BookModel).all()
    return result

@router.get("/personal_books/{book_id}", response_model=BookResponseSchema)
async def retrieve_the_targeted_personal_books(book_id: int = Path(..., gt = 0), db: Session = Depends(get_db)):
    result = db.query(BookModel).filter(BookModel.id == book_id).first()
    if not result:
        raise HTTPException(status_code=404, detail="Book not found")
    return result

@router.post("/personal_books")
async def create_a_new_book(book: BookCreateSchema, db: Session = Depends(get_db)):
    new_book = BookModel(**book.model_dump())
    db.add(new_book)
    db.commit()
    db.refresh(new_book)
    return JSONResponse(status_code=201, content={"message": "Book created successfully", "book_id": new_book.id})

@router.put("/personal_books/{book_id}", response_model=BookResponseSchema)
async def update_a_book(book: BookUpdateSchema, book_id: int = Path(..., gt = 0), db: Session = Depends(get_db)):
    result = db.query(BookModel).filter(BookModel.id == book_id).first()
    if not result:
        raise HTTPException(status_code=404, detail="Book not found")
    for key, value in book.model_dump().items():
        setattr(result, key, value)
    db.commit()
    db.refresh(result)
    return result

@router.delete("/personal_books/{book_id}", status_code=204)
async def delete_a_book(book_id: int = Path(..., gt = 0), db: Session = Depends(get_db)):
    result = db.query(BookModel).filter(BookModel.id == book_id).first()
    if not result:
        raise HTTPException(status_code=404, detail="Book not found")
    db.delete(result)
    db.commit()
    return JSONResponse(status_code=204, content={"message": "Book deleted successfully"})