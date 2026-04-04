from fastapi import FastAPI, status, Depends
from sqlalchemy.orm import Session
from fastapi.exceptions import HTTPException
from schema import Books, BookUpdate
import models
from database import engine, get_db

# Create the database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/book")
def get_books(db: Session = Depends(get_db)):
    books = db.query(models.Book).all()
    return books

@app.post("/book", status_code=status.HTTP_201_CREATED)
def create_book(book: Books, db: Session = Depends(get_db)):
    db_book = models.Book(**book.model_dump())
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book

@app.get("/book/{book_id}")
def get_book_by_id(book_id: int, db: Session = Depends(get_db)):
    book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
    return book

@app.put("/book/{book_id}")
def update_book(book_id: int, book_update: BookUpdate, db: Session = Depends(get_db)):
    db_book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if not db_book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
    
    db_book.title = book_update.title
    db_book.author = book_update.author
    db_book.price = book_update.price
    
    db.commit()
    db.refresh(db_book)
    return db_book

@app.delete("/book/{book_id}")
def delete_book(book_id: int, db: Session = Depends(get_db)):
    db_book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if not db_book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
    
    db.delete(db_book)
    db.commit()
    return {"Message": f"Book id {book_id} removed"}




