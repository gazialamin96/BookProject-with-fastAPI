from typing import Optional

from fastapi import FastAPI, Path, Query, HTTPException
# pydentic is a framework that allows us to validate to our data
# BaseModel is a model when object coming in that will be validated the data
from pydantic import BaseModel, Field
from starlette import status

app = FastAPI()


class Book:
    identification: int
    title: str
    author: str
    description: str
    rating: int
    published_date: int

    def __init__(self, identification, title, author, description, rating, published_dates):
        self.identification = identification
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating
        self.published_date = published_dates


# pydantic Object
class BookRequest(BaseModel):
    identification: Optional[int]
    title: str = Field(min_length=3)
    author: str = Field(min_length=1)
    description: str = Field(min_length=1, max_length=100)
    rating: int = Field(gt=0, lt=6)
    published_date: int = Field(gt=1999, lt=2031)

    # Show the example of schema it's a pydentic class
    class Config:
        json_schema_extra = {
            'example': {
                "identification": 1,
                "title": "Architecture",
                "author": "Shakil Khan",
                "description": "Good Books",
                "rating": 3,
                "published_date": 2023
            }
        }


BOOKS = [
    Book(1, 'Computer Science', 'Gazi Al- Amin', 'Good Book', 5, 2023),
    Book(2, 'Automobile Engineering', 'Gazi Arman', 'Authentic Book', 4, 2022),
    Book(3, 'Computer Science', 'Gazi Al- Amin', 'Nice Book', 5, 2001),
    Book(4, 'Micro Economics', 'Mahfuja Mitu', 'Real World Economics', 4, 2022),
    Book(5, 'Architecture', 'Shakil Khan', 'Good Books', 2,  2001)
]


# read/ get books
@app.get("/books", status_code=status.HTTP_200_OK)
async def read_all_books():
    return BOOKS


# book search by ID
@app.get("/books/{book_id}", status_code=status.HTTP_200_OK)
# path validation of int = Path(gt=0) "input should be greater than 0"
async def read_book(book_id: int = Path(gt=0)):
    for book in BOOKS:
        if book.identification == book_id:
            return book
    raise HTTPException(status_code=404, detail="Books Not Found")


# create a new GET Request method to filter by published_date
@app.get("/books/publish/", status_code=status.HTTP_200_OK)
async def published_date(book_published_date: int = Query(gt=1999, lt=2031)):
    books_to_return = []
    for book in BOOKS:
        if book.published_date == book_published_date:
            books_to_return.append(book)
    return books_to_return


# filter by Book Rating
@app.get("/books/", status_code=status.HTTP_200_OK)
# Query Parameter validation Query(gt=0, lt=6)
async def read_book_by_rating(book_rating: int = Query(gt=0, lt=6)):
    books_to_return = []
    for book in BOOKS:
        if book.rating == book_rating:
            books_to_return.append(book)
    return books_to_return


# create/ post book
@app.post("/create-book", status_code=status.HTTP_201_CREATED)
async def create_book(book_request: BookRequest):
    new_book = Book(**book_request.model_dump())
    BOOKS.append(find_book_id(new_book))


# Identifications validation
def find_book_id(book: Book):
    if len(BOOKS) > 0:
        book.identification = BOOKS[-1].identification + 1
    else:
        book.identification = 1

    return book


# update/ PUT Enhance Books with PUT Request method
@app.put("/books/update_book", status_code=status.HTTP_204_NO_CONTENT)
async def update(book: BookRequest):
    book_changed = False
    for i in range(len(BOOKS)):
        if BOOKS[i].identification == book.identification:
            BOOKS[i] = book
            book_changed = True
    if not book_changed:
        raise HTTPException(status_code=404, detail="Item not Found!")


# delete Books with delete Request method
@app.delete("/books/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
# path validation of int = Path(gt=0) "input should be greater than 0"
async def delete_book(book_id: int = Path(gt=0)):
    book_changed = False
    for i in range(len(BOOKS)):
        if BOOKS[i].identification == book_id:
            BOOKS.pop(i)
            book_changed = True
            break
    if not book_changed:
        raise HTTPException(status_code=404, detail="Item Not Found")


