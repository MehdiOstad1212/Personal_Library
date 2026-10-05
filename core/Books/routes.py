from fastapi import APIRouter

router = APIRouter(tags=["personal_library"])

@router.get("/books")
async def retrieve_the_whole_books():
    return []

@router.get("/books/{book_id}")
async def retrieve_the_targeted_book():
    return []

@router.get("/personal_books")
async def retrieve_the_whole_personal_books():
    return []

@router.get("/personal_books/{book_id}")
async def retrieve_the_targeted_personal_books():
    return []