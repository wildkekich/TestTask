from .Book import Book
from typing import List
import json
from src.loggers.loggers import db_logger_wrap


class BookDatabase:
    def __init__(self, path):
        self.file = path

    @db_logger_wrap
    def insert(self, new_book: Book):
        try:
            with open(self.file, "r") as f:
                all_data = json.loads(f.read())
                if isinstance(all_data, dict):
                    all_data = [all_data]
        except FileNotFoundError:
            all_data = []
        except json.JSONDecodeError:
            all_data = []

        all_data.append(new_book.to_dict())
        with open(self.file, "w") as f:
            f.write(json.dumps(all_data, indent=4))

    def read(self) -> List[Book]:
        try:
            with open(self.file, "r") as f:
                all_data = json.loads(f.read())
            books = []
            for item in all_data:
                for book_id, book_data in item.items():
                    books.append(Book(book_id, book_data))

            return books
        except Exception as e:
            raise RuntimeError(f"{e}")

    @db_logger_wrap
    def update(self, id: str, new_book: Book) -> None:
        try:
            books = self.read()
            for book in books:
                if book.id == id:
                    index = books.index(book)
                    books.remove(book)
                    books.insert(index, new_book)

            books_dict = [book.to_dict() for book in books]
            with open(self.file, "w") as f:
                f.write(json.dumps(books_dict, indent=4))
        except Exception as e:
            raise RuntimeError(f"{e}")

    @db_logger_wrap
    def delete(self, id: str) -> None:
        try:
            books = self.read()
            for book in books:
                if book.id == id:
                    books.remove(book)
            books_dict = [book.to_dict() for book in books]
            with open(self.file, "w") as f:
                f.write(json.dumps(books_dict, indent=4))
        except Exception as e:
            raise RuntimeError(f"{e}")
