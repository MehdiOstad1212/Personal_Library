from fastapi import APIRouter, Depends, HTTPException, Path, Query
from Books.models import BookModel
from Books.schemas import *
from sqlalchemy.orm import Session
from core.database import get_db
from typing import List
from fastapi.responses import JSONResponse
from auth.jwt_auth import get_authenticated_user
from users.models import UserModel

router = APIRouter(tags=["personal_library"])

@router.get("/books", response_model=List[BookNameandAuthorResponseSchema])
async def retrieve_the_whole_books(
                    limit: int = Query(10, gt=0, le=50,
                            description="Limit the number of books returned"),
                        offset: int = Query(0, ge=0,
                            description="Offset for pagination"),
                        db: Session = Depends(get_db),
                        user: UserModel = Depends(get_authenticated_user)):
    #only the name of the book and the author will be returned and sorted by the number_of_readers in descending order
    result = db.query(BookModel.title_of_the_book, BookModel.author, BookModel.number_of_readers).order_by(BookModel.number_of_readers.desc()).offset(offset).limit(limit).all()
    # Deleting the repetitive books with the same title and author, only the first one will be returned with its number_of_readers
    unique_books = {}
    for book in result:
        if book.title_of_the_book not in unique_books:
            unique_books[book.title_of_the_book] = book
    return list(unique_books.values())

@router.get("/books/{author}", response_model=List[AuthorFilteredResponseSchema])
async def retrieve_the_targeted_book(author: str = Path(..., max_length=100, description="The author of the book"),
                                     db: Session = Depends(get_db),
                                     user: UserModel = Depends(get_authenticated_user)):
    # only the name of the book and the author will be returned and the lowercase of the author will be used to filter the books and the result will be sorted by the number_of_readers in descending order
    result = db.query(BookModel.title_of_the_book, BookModel.number_of_readers).filter(BookModel.author == author.lower()).all()
    if not result:
        raise HTTPException(status_code=404, detail="details for this author not found")
    # Deleting the repetitive books with the same title and author, only the last one will be returned with its number_of_readers
    unique_books = {}
    for book in result:
        unique_books[book.title_of_the_book] = book
    # Sorting the unique books by the number_of_readers in descending order
    unique_books = dict(sorted(unique_books.items(), key=lambda item: item[1].number_of_readers, reverse=True))
    return list(unique_books.values())

@router.get("/personal_books", response_model=List[BookResponseSchema])
async def retrieve_the_whole_personal_books(
                        completed: bool = Query(None,
                            description="Filter books by completion status"),
                        limit: int = Query(10, gt=0, le=20,
                            description="Limit the number of books returned"),
                        offset: int = Query(0, ge=0,
                            description="Offset for pagination"),
                        db: Session = Depends(get_db),
                        user: UserModel = Depends(get_authenticated_user)):
    result = db.query(BookModel).filter_by(user_id = user.id)
    if completed is not None:
        result = result.filter_by(is_completed = completed)
    return result.offset(offset).limit(limit).all()

@router.get("/personal_books/{book_id}", response_model=BookResponseSchema)
async def retrieve_the_targeted_personal_books(book_id: int = Path(..., gt = 0), db: Session = Depends(get_db), user: UserModel = Depends(get_authenticated_user)):
    result = db.query(BookModel).filter(BookModel.id == book_id, BookModel.user_id == user.id).first()
    if not result:
        raise HTTPException(status_code=404, detail="Book not found")
    return result

@router.post("/personal_books")
async def create_a_new_book(book: BookCreateSchema,
                            db: Session = Depends(get_db),
                            user: UserModel = Depends(get_authenticated_user)):
    data = book.model_dump()
    if db.query(BookModel).filter_by(title_of_the_book=data["title_of_the_book"].lower(), author=data["author"].lower(), user_id=user.id).first():
        raise HTTPException(status_code=409, detail="Book with this title and author already exists in your personal library")
    # the last book with the same title and author will be retrieved to update the number_of_readers
    result = db.query(BookModel).filter_by(title_of_the_book=data["title_of_the_book"].lower(), author=data["author"].lower()).all()  # get the last book with the same title and author
    if result:
        new_result = result[-1].number_of_readers + 1
    data.update({"user_id": user.id,
                 "number_of_readers": new_result if result else 1,
                 "title_of_the_book": data["title_of_the_book"].lower(),
                 "author": data["author"].lower(),
                 "is_completed": False if data["number_of_reads"] == 0 else True})
    new_book = BookModel(**data)
    db.add(new_book)
    db.commit()
    db.refresh(new_book)
    return JSONResponse(status_code=201, content={"message": "Book created successfully", "book_id": new_book.id})

@router.put("/personal_books/{book_id}", response_model=BookResponseSchema)
async def update_a_book(book: BookUpdateSchema, book_id: int = Path(..., gt = 0),
                        db: Session = Depends(get_db),
                        user: UserModel = Depends(get_authenticated_user)):
    result = db.query(BookModel).filter(BookModel.id == book_id, BookModel.user_id == user.id).first()
    if not result:
        raise HTTPException(status_code=404, detail="Book not found")
    data = book.model_dump()
    # If the number_of_reads is updated to 0, the book will be marked as not completed, otherwise it will be marked as completed
    if book.number_of_reads == 0:
        data.update({"is_completed": False})
    # If the number_of_reads is updated to a value greater than 0, the book will be marked as completed
    elif book.number_of_reads > 0:
        data.update({"is_completed": True})
    for key, value in data.items():
        setattr(result, key, value)
    db.commit()
    db.refresh(result)
    return result

@router.delete("/personal_books/{book_id}", status_code=204)
async def delete_a_book(book_id: int = Path(..., gt = 0),
                        db: Session = Depends(get_db),
                        user: UserModel = Depends(get_authenticated_user)):
    result = db.query(BookModel).filter(BookModel.id == book_id, BookModel.user_id == user.id).first()
    if not result:
        raise HTTPException(status_code=404, detail="Book not found")
    db.delete(result)
    db.commit()
    return JSONResponse(status_code=204, content={"message": "Book deleted successfully"})