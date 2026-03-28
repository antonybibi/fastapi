from pydantic import BaseModel


class Books(BaseModel):
    id: int
    title: str
    author: str
    isbn: str
    price: float


class BookUpdate(BaseModel):
    title: str
    author: str
    price: float


