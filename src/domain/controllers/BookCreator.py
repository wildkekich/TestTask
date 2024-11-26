from ..models.Book import Book
from ..models.BookDatabase import BookDatabase
import time


class BookCreator:
    _book_db: BookDatabase

    def __init__(self, books: BookDatabase):
        self._book_db = books

    def create(self, author: str, title: str, year: int, id: str = None, status: bool = None) -> Book:
        try:
            if id is None:
                id = hex(int(time.time()))
            if status is None:
                status = True

            book = Book(id, {
                "author": author,
                "title": title,
                "year": year,
                "status": status,
            })
            self._book_db.insert(book)
            return book
        except Exception as e:
            raise RuntimeError(f"{e}")
