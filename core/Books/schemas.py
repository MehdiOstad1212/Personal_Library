from datetime import datetime

from pydantic import BaseModel, Field
from typing import Optional

class BookBase(BaseModel):
    title_of_the_book: str = Field(..., max_length=200, description="The title of the book")
    author: str = Field(..., max_length=100, description="The author of the book")
    description: Optional[str] = Field(None, max_length=500, description="A brief description of the book")
    is_completed: bool = Field("False", description="Indicates whether the book has been completed")

class BookCreateSchema(BookBase):
    pass

class BookUpdateSchema(BookBase):
    pass

class BookResponseSchema(BookBase):
    id: int = Field(..., description="The unique identifier of the book")
    created_at: datetime = Field(..., description="The timestamp when the book was created")
    updated_at: datetime = Field(..., description="The timestamp when the book was last updated")


class BookNameandAuthorResponseSchema(BaseModel):
    title_of_the_book: str = Field(..., max_length=200, description="The title of the book")
    author: str = Field(..., max_length=100, description="The author of the book")