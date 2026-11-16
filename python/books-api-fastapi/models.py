from sqlalchemy import Boolean, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Author(Base):
    __tablename__ = 'authors'

    id = Column(Integer, primary_key=True, index=True)
    last_name = Column(String(100), nullable=False)
    first_name = Column(String(100), nullable=False)
    middle_name = Column(String(100), nullable=True)

    books = relationship("Book", back_populates="author")

class Book(Base):
    __tablename__ = 'books'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(250))
    stock_quantity = Column(Integer, nullable=False, default=0, server_default="0")
    author_id = Column(Integer, ForeignKey('authors.id'), nullable=True)

    author = relationship("Author", back_populates="books")
