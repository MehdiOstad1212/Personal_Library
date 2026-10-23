from datetime import datetime

from pydantic import BaseModel, Field
from typing import Optional

class BookBase(BaseModel):
    title_of_the_book: str = Field(..., max_length=200, description="The title of the book")
    author: str = Field(..., max_length=100, description="The author of the book")
    description: Optional[str] = Field(None, max_length=500, description="A brief description of the book")
    number_of_reads: int = Field(..., description = "how many times have you read this particular book?")

class BookCreateSchema(BookBase):
    pass

class BookUpdateSchema(BaseModel):
    description: Optional[str] = Field(None, max_length=500, description="A brief description of the book")
    number_of_reads: int = Field(..., description = "how many times have you read this particular book?")

class BookResponseSchema(BaseModel):
    title_of_the_book: str = Field(..., max_length=200, description="The title of the book")
    author: str = Field(..., max_length=100, description="The author of the book")
    id: int = Field(..., description="The unique identifier of the book")
    description: Optional[str] = Field(None, max_length=500, description="A brief description of the book")
    is_completed: bool = Field("False", description="Indicates whether the book has been completed")
    number_of_reads: int = Field(..., description = "how many times have you read this particular book?")
    created_at: datetime = Field(..., description="The timestamp when the book was created")
    updated_at: datetime = Field(..., description="The timestamp when the book was last updated")


class AuthorFilteredResponseSchema(BaseModel):
    title_of_the_book: str = Field(..., max_length=200, description="The title of the book")
    number_of_readers: int = Field(..., description="The number of readers for the book")

class BookNameandAuthorResponseSchema(BaseModel):
    title_of_the_book: str = Field(..., max_length=200, description="The title of the book")
    author: str = Field(..., max_length=100, description="The author of the book")
    number_of_readers: int = Field(..., description="The number of readers for the book")