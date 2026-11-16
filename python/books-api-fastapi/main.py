from fastapi import FastAPI, HTTPException, Depends, status
from pydantic import BaseModel, model_validator
from typing import Annotated
import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session

app = FastAPI()
models.Base.metadata.create_all(bind=engine)

class BookCreate(BaseModel):
    title: str
    author_id: int | None = None
    last_name: str | None = None
    first_name: str | None = None
    middle_name: str | None = None

@model_validator(mode="after")
def check_author_fields(self):
        # None or 0 means "author does not exist yet"
        if not self.author_id:
            if not self.last_name or not self.first_name or not self.middle_name:
                raise ValueError(
                    "last_name, first_name and middle_name are required when author_id is empty or 0"
                )
        return self

class StockUpdate(BaseModel):
    quantity: int

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

@app.get("/")
def root():
    return {"hello": "world"}

# add book entry. author fields can be existing or new. if existing, insert valid author id
@app.post("/books/", status_code=status.HTTP_201_CREATED)
def create_book(book: BookCreate, db: db_dependency):
    if book.author_id:
        author = db.query(models.Author).filter(models.Author.id == book.author_id).first()
        if author is None:
            raise HTTPException(status_code=404, detail="Author not found")
    else:
        author = models.Author(
            last_name=book.last_name,
            first_name=book.first_name,
            middle_name=book.middle_name,
        )
        db.add(author)
        db.flush()  # sends the INSERT so author.id is available, without committing yet

    db_book = models.Book(title=book.title, author_id=author.id)
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return book_response(db_book)

# get book entry via book id 
@app.get("/books/{book_id}", status_code=status.HTTP_200_OK)
async def get_book(book_id: int, db:db_dependency):
    book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return book_response(book)

# add stock quantity to selected book
@app.post("/books/{book_id}/stock", status_code=status.HTTP_200_OK)
def add_stock_quantity(book_id: int, stock: StockUpdate, db: db_dependency):
    book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")

    new_quantity = book.stock_quantity + stock.quantity
    if new_quantity < 0:
        raise HTTPException(status_code=400, detail="Stock cannot go below 0")

    book.stock_quantity = new_quantity
    db.commit()
    db.refresh(book)

    return book_response(book)

# helper function to get stock status
def get_stock_status(quantity: int) -> str:
    if quantity <= 0:
        return "OUT_OF_STOCK"
    if quantity <= 5:
        return "LOW_STOCK"
    return "IN_STOCK"
# helper function for uniform response
def book_response(book: models.Book) -> dict:
    author = book.author
    return {
        "book": {
            "id": book.id,
            "title": book.title,
            "stock_quantity": book.stock_quantity,
            "stock_status": get_stock_status(book.stock_quantity),
            "author": {
                "last_name": author.last_name,
                "first_name": author.first_name,
                "middle_name": author.middle_name,
            } if author else None,
        }
    }