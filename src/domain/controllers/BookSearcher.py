from ..models.BookDatabase import BookDatabase
from typing import List
from ..models.Book import Book


class BookSearcher:
    _books_db: BookDatabase

    def __init__(self, books_db: BookDatabase):
        self._books_db = books_db

    def by_author(self, author: str) -> List[Book]:
        try:
            return [book for book in self._books_db.read() if book.author == author]
        except Exception as e:
            raise RuntimeError(f"{e}")

    def by_title(self, title: str) -> List[Book]:
        try:
            return [book for book in self._books_db.read() if book.title == title]
        except Exception as e:
            raise RuntimeError(f"{e}")

    def by_year(self, year: int) -> List[Book]:
        try:
            return [book for book in self._books_db.read() if book.year == year]
        except Exception as e:
            raise RuntimeError(f"{e}")

    def by_id(self, id: str) -> Book:
        try:
            for book in self._books_db.read():
                if book.id == id:
                    return book
        except Exception as e:
            raise RuntimeError(f"{e}")

    def by_range(self, num_from: int, num_to: int) -> List[Book]:
        try:
            return self._books_db.read()[num_from:num_to]
        except Exception as e:
            raise RuntimeError(f"{e}")

    def get_total(self):
        try:
            return len(self._books_db.read())
        except Exception as e:
            raise RuntimeError(f"{e}")
