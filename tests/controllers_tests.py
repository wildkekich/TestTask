import unittest
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
import random

from src.domain.models.Book import Book
from src.domain.models.BookDatabase import BookDatabase
from src.domain.controllers.BookSearcher import BookSearcher
from src.domain.controllers.BookCreator import BookCreator
from src.domain.controllers.BookDeleter import BookDeleter
from src.domain.controllers.BookEditor import BookEditor

path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "other/testdatabase.json")
book_db = BookDatabase(path)
book_searcher = BookSearcher(book_db)
book_creator = BookCreator(book_db)
book_editor = BookEditor(book_db)
book_deleter = BookDeleter(book_db)


def cleanup_db():
    all_books = book_searcher.by_range(0, 200)
    for book in all_books:
        book_deleter.delete(book.id)


def generate_books(test: str):
    return [Book(f"{test}someid{x}", {
                          "author": f"SomeFamousDude{x}",
                          "title": f"SomeCoolTitle{x}",
                          "year": 2000 + x,
                          "status": True}) for x in range(10)]


class BookSearcherTest(unittest.TestCase):

    def test_search_by_id(self):
        books = generate_books("SEARCH:ID")
        book_to_insert = random.choice(books)
        self.assertEqual(book_searcher.by_id(book_to_insert.id), None)
        for book in books:
            book_db.insert(book)
        self.assertEqual(book_searcher.by_id(book_to_insert.id), book_to_insert)

    def test_search_by_author(self):
        cleanup_db()
        books = generate_books("SEARCH:AUTHOR")
        book_to_insert = random.choice(books)
        self.assertEqual(book_searcher.by_author(book_to_insert.author), [])
        for book in books:
            book_db.insert(book)
        self.assertEqual(book_searcher.by_author(book_to_insert.author), [book_to_insert])

    def test_search_by_title(self):
        cleanup_db()
        books = generate_books("SEARCH:TITLE")
        book_to_insert = random.choice(books)
        self.assertEqual(book_searcher.by_title(book_to_insert.title), [])
        for book in books:
            book_db.insert(book)
        self.assertEqual(book_searcher.by_title(book_to_insert.title), [book_to_insert])

    def test_search_by_year(self):
        cleanup_db()
        books = generate_books("SEARCH:YEAR")
        book_to_insert = random.choice(books)
        self.assertEqual(book_searcher.by_year(book_to_insert.year), [])
        for book in books:
            book_db.insert(book)
        self.assertEqual(book_searcher.by_year(book_to_insert.year), [book_to_insert])


class BookInserterTest(unittest.TestCase):
    def test_insert_book(self):
        book = Book(id="INSERT", kwargs={
            "author": "SomeAuthor",
            "title": "SomeTitle",
            "year": 2024,
            "status": True
        })

        self.assertEqual(book_searcher.by_id(book.id), None)
        self.assertEqual(book_searcher.by_author(book.author), [])
        self.assertEqual(book_searcher.by_title(book.title), [])
        self.assertEqual(book_searcher.by_year(book.year), [])

        new_book = book_creator.create(author="SomeAuthor", title="SomeTitle", year=2024, id="INSERT", status=True)

        self.assertEqual(book, new_book)

        self.assertEqual(book_searcher.by_id("INSERT"), book)
        self.assertEqual(book_searcher.by_author("SomeAuthor"), [book])
        self.assertEqual(book_searcher.by_year(2024), [book])
        self.assertEqual(book_searcher.by_title("SomeTitle"), [book])


class BookEditorTest(unittest.TestCase):
    def test_edit_book(self):
        books = generate_books("EDIT:ALL")

        for book in books:
            self.assertEqual(book_searcher.by_id(book.id), None)
            book_db.insert(book)

        for book in books:
            self.assertEqual(book_searcher.by_id(book.id), book)
            book_editor.edit(id=book.id, new_author="NEWAUTHORFORALLBOOKS",
                             new_title=book.title, new_year=book.year,
                             new_status=not book.status)
        for book in books:
            self.assertEqual(book_searcher.by_id(book.id).status, False)
            self.assertEqual(book_searcher.by_id(book.id).author, "NEWAUTHORFORALLBOOKS")

    def test_edit_only_status(self):
        books = generate_books("EDIT:STATUS")

        for book in books:
            self.assertEqual(book_searcher.by_id(book.id), None)
            book_db.insert(book)

        for book in books:
            self.assertEqual(book_searcher.by_id(book.id), book)
            book_editor.edit_status_only(book.id)

        for book in books:
            self.assertEqual(book_searcher.by_id(book.id).status, False)


class BookDeleterTest(unittest.TestCase):
    def test_delete_book(self):
        books = generate_books("DELETE")

        for book in books:
            self.assertEqual(book_searcher.by_id(book.id), None)
            book_db.insert(book)

        for book in books:
            self.assertEqual(book_searcher.by_id(book.id), book)
            book_deleter.delete(book.id)
            self.assertEqual(book_searcher.by_id(book.id), None)
