from sqlalchemy import Column, String, Text, Boolean, func, Integer, DateTime, ForeignKey
from core.database import Base
from sqlalchemy.orm import relationship


class BookModel(Base):
    __tablename__ = "books"
    id = Column(Integer,
                primary_key = True,
                autoincrement = True)
    title_of_the_book = Column(String(200), nullable = False)
    author = Column(String(100), nullable = False)
    description = Column(Text(500), nullable = True)
    is_completed = Column(Boolean, default=False)
    created_at = Column(DateTime(), server_default=func.now())
    updated_at = Column(DateTime(),
                        server_default=func.now(),
                        server_onupdate=func.now())

    user = relationship("UserModel", back_populates="books", uselist = False)
    user_id = Column(Integer, ForeignKey("users.id"))