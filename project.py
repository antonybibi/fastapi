from fastapi import FastAPI, Depends, HTTPException, status
from database import get_db, engine
from sqlalchemy.orm import Session
import model
import schema

app = FastAPI()

@app.post("/books")
def create_book(book: schema.BookStore, db: Session = Depends(get_db)):
    exists = db.query(model.Book).filter(
        (model.Book.id == book.id) | (model.Book.isbn == book.isbn)
    ).first()
    
    if exists:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Book already exists")
    new_book = model.Book(id=book.id, title = book.title, author = book.author, isbn = book.isbn, price = book.price)

    db.add(new_book)
    db.commit()
    db.refresh(new_book)
    return new_book


@app.get("/books")
def get_book(db:Session = Depends(get_db)):
    books = db.query(model.Book).all()
    return books