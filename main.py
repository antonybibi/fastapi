from fastapi import FastAPI
from typing import Optional
from pydantic import BaseModel

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello World"}


@app.get("/greet")
def greet():
    return {"message": "Hello, Antony!"}

# path parameters
@app.get("/greet/{name}")
def greet_name(name: str): # since the validation is already done by the type hint if we add any other type it will throw an error
    return {"message": f"Hello, {name}!"}

# query parameters
@app.get("/greets")
def greet_name(name: str, age: Optional[int] = 10):
    return {"message": f"{name} is {age} years old"}

class Student(BaseModel):
    name: str
    age: int
    roll: int

class StudentReturn(BaseModel): # for post and put method we have to use this pydantic model
    name: str
    age: int
    roll: int


@app.post("/create_student")
def create_student(student: Student) -> StudentReturn: 
    return StudentReturn(
        name = student.name,
        age = student.age,
        roll = student.roll
    )



