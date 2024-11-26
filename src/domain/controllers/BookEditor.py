from ..models.Book import Book
from ..models.BookDatabase import BookDatabase


class BookEditor:
    _book_db: BookDatabase

    def __init__(self, books: BookDatabase):
        self._book_db = books

    def edit(self, id: str, new_author: str, new_title: str, new_year: int, new_status: bool) -> bool:
        try:
            for book in self._book_db.read():
                if book.id == id:
                    new_book = Book(id, {
                         "author": new_author,
                         "title": new_title,
                         "year": new_year,
                         "status": new_status
                    })
                    self._book_db.update(id, new_book)
                    return True
            return False
        except Exception as e:
            raise RuntimeError(f"{e}")

    def edit_status_only(self, id: str):
        try:
            for book in self._book_db.read():
                if book.id == id:
                    book.status = not book.status
                    self._book_db.update(id, book)
                    return True
            return False
        except Exception as e:
            raise RuntimeError(f"{e}")