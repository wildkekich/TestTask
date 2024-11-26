import unittest
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from src.domain.models.Book import Book
from src.domain.models.BookDatabase import BookDatabase

path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "other/testdatabase.json")


def get_books(test: str):
    return [Book(f"{test}someid{x}", {
                          "author": f"SomeFamousDude{x}",
                          "title": f"SomeCoolTitle{x}",
                          "year": 2000 + x,
                          "status": True}) for x in range(10)]


class TestDatabase(unittest.TestCase):

    def test1_insert_and_read_multiple_books(self):
        book_db = BookDatabase(path)

        books_to_insert = get_books("INSERT/READ")

        for book in books_to_insert:
            book_db.insert(new_book=book)

        books_in_db = book_db.read()

        size_of_db = len(books_in_db)
        size_of_books_to_insert = len(books_to_insert)
        index = size_of_db - size_of_books_to_insert

        for book in books_to_insert:
            self.assertEqual(book, books_in_db[index])
            index = index + 1

    def test2_edit_book(self):
        book_db = BookDatabase(path)

        books_to_update = get_books("EDIT")

        for book in books_to_update:
            book_db.insert(book)

        for book in books_to_update:
            book.title = book.title.upper()
            book.status = not book.status

        for book in books_to_update:
            book_db.update(book.id, book)

        books_in_db = book_db.read()
        size_of_db = len(books_in_db)
        size_of_books_to_insert = len(books_to_update)
        index = size_of_db - size_of_books_to_insert

        for book in books_to_update:
            self.assertEqual(book, books_in_db[index])
            index = index + 1

    def test3_delete_book(self):
        book_db = BookDatabase(path)

        books_to_delete = get_books("TODELETE")

        for book in books_to_delete:
            book_db.insert(book)

        for book in books_to_delete:
            self.assertTrue(book_db.read().__contains__(book))

        cmd = input("Continue...")
        for book in books_to_delete:
            book_db.delete(book.id)

        for book in books_to_delete:
            self.assertTrue(not book_db.read().__contains__(book))
