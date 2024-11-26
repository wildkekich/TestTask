from ..models.BookDatabase import BookDatabase


class BookDeleter:
    _book_db: BookDatabase

    def __init__(self, books: BookDatabase):
        self._book_db = books

    def delete(self, id: str):
        try:
            for book in self._book_db.read():
                if book.id == id:
                    self._book_db.delete(id)
                    return True, book
            return False, None
        except Exception as e:
            raise RuntimeError(f"{e}")
