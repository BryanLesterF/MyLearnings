from fastapi import FastAPI, HTTPException, Depends, status
from pydantic import BaseModel
from typing import Annotated
import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session

app = FastAPI()
models.Base.metadata.create_all(bind=engine)

class BookBase(BaseModel):
    title:str

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

@app.post("/books/", status_code=status.HTTP_201_CREATED)
async def create_book(book:BookBase, db:db_dependency):
    db_book = models.Book(**book.model_dump())
    db.add(db_book)
    db.commit()

@app.get("/books/{book_id}", status_code=status.HTTP_200_OK)
async def get_book(book_id: int, db:db_dependency):
    book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return {
        "book": {
            "id": book.id,
            "title": book.title,
            "stock_quantity": book.stock_quantity,
            "stock_status": get_stock_status(book.stock_quantity)
        }
    }

def get_stock_status(quantity: int) -> str:
    if quantity <= 0:
        return "OUT_OF_STOCK"
    if quantity <= 5:
        return "LOW_STOCK"
    return "IN_STOCK"
