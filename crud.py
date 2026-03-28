from fastapi import FastAPI, status
from pydantic import BaseModel
from fastapi.exceptions import HTTPException
from schema import Books, BookUpdate


books = [
    {
        "id": 1,
        "title": "Book 1",
        "author": "Author 1",
        "isbn": "1234567890",
        "price": 10.99
    },
    {
        "id": 2,
        "title": "Book 2",
        "author": "Author 2",
        "isbn": "1234567891",
        "price": 11.99
    },
    {
        "id": 3,
        "title": "Book 3",
        "author": "Author 3",
        "isbn": "1234567892",
        "price": 12.99
    }
]

app = FastAPI()


@app.get("/book")
def get_book():
    return books



@app.post("/book")
def create_book(book: Books):
    new_book = book.model_dump()
    books.append(new_book)
    return new_book


@app.get("/book/{book_id}")
def get_book_by_id(book_id: int):
    for book in books:
        if book.get("id") == book_id:
            return book
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")


@app.put("/book/{book_id}")
def update_book(book_id: int, book_update: BookUpdate):
    for book in books:
        if book.get("id") == book_id:
            book['title'] = book_update.title
            book['author'] = book_update.author
            book['price'] = book_update.price
            return book
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")


@app.delete("/book/{book_id}")
def delete_book(book_id : int):
    for book in books:
        if book["id"] == book_id:
            books.remove(book)
            return {"Message": f"Book id{book_id} removed"}

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")




