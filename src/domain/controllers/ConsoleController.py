import os
from typing import List
from .BookSearcher import BookSearcher
from .BookEditor import BookEditor
from .BookCreator import BookCreator
from .BookDeleter import BookDeleter
from ..models.BookDatabase import BookDatabase
from src.views.ConsoleView import ConsoleView


class ConsoleController:
    book_searcher: BookSearcher
    book_deleter: BookDeleter
    book_creator: BookCreator
    book_editor: BookEditor
    console_view: ConsoleView
    page: int
    to_show_on_page: int
    exit: bool

    def __init__(self, bs: BookSearcher, bc: BookCreator, bd: BookDeleter, be: BookEditor, cv: ConsoleView):
        self.book_deleter = bd
        self.book_creator = bc
        self.book_searcher = bs
        self.book_editor = be
        self.console_view = cv
        self.to_show_on_page = 10
        self.page = 1
        self.exit = False

    def main(self):
        while not self.exit:
            self.get_user_input()
            books_to_show = self.book_searcher.by_range(num_from=(self.page - 1) * self.to_show_on_page,
                                                        num_to=self.page * self.to_show_on_page)
            self.console_view.show(books_to_show, self.page)

    def get_user_input(self):
        try:
            user_input = input("Execute: ")

            if user_input.startswith("exit"):
                self.exit = True

            elif user_input.startswith("if"):
                message, new_books = self.insert_file(user_input.split(" "))
                self.console_view.react_to_user_interaction(message, new_books)

            elif user_input.startswith("i"):
                message, new_book = self.insert(user_input.split(";"))
                self.console_view.react_to_user_interaction(message, new_book)

            elif user_input.startswith("s"):
                message, found_books = self.search(user_input.split(";"))
                self.console_view.react_to_user_interaction(message, found_books)

            elif user_input.startswith("e"):
                message, edited_book = self.edit(user_input.split(";"))
                self.console_view.react_to_user_interaction(message, edited_book)

            elif user_input.startswith("d"):
                message, deleted_book = self.delete(user_input.split(" "))
                self.console_view.react_to_user_interaction(message, deleted_book)

            elif user_input.startswith(">"):
                self.next_page()
            elif user_input.startswith("<"):
                self.prev_page()
            elif user_input.startswith("c"):
                self.change_table(user_input.split(" "))
            else:
                self.console_view.show_menu()
        except Exception as e:
            raise RuntimeError(f"{e}")



    def insert(self, user_command: List[str]):
        try:
            if len(user_command) != 4:
                return "ERROR. Three fields are required for making a new entry.", []

            new_book = self.book_creator.create(author=user_command[1].strip(),
                                                title=user_command[2].strip(),
                                                year=int(user_command[3].strip()))
            return "SUCCESS.", [new_book]
        except Exception as e:
            raise RuntimeError(f"{e}")

    def insert_file(self, user_command: List[str]):
        try:
            if len(user_command) != 2:
                return "ERROR. You need to pass the path of an existing file.", []
            added = []
            try:
                if os.path.exists(user_command[1].strip()):
                    new_db = BookDatabase(user_command[1].strip())
                    books = new_db.read()
                    for book in books:
                        self.book_creator.create(author=book.author, title=book.title,
                                                 year=book.year, id=book.id, status=book.status)
            except Exception as e:
                return f"ERROR. Data in the file doesn't match with json format.{e}"
            return "SUCCESS.", added
        except Exception as e:
            raise RuntimeError(f"{e}")

    def search(self, user_command: List[str]):
        try:
            if len(user_command) != 3:
                return "ERROR. Two fields are required for searching an entry.", []
            if user_command[1].strip().lower() == "author":
                found = self.book_searcher.by_author(user_command[2].strip())
                return "SUCCESS." if len(found) > 0 else "THERE ARE NO MATCHES", found
            if user_command[1].strip().lower() == "title":
                found = self.book_searcher.by_title(user_command[2].strip())
                return "SUCCESS." if len(found) > 0 else "THERE ARE NO MATCHES", found
            if user_command[1].strip().lower() == "year":
                found = self.book_searcher.by_year(int(user_command[2].strip()))
                return "SUCCESS." if len(found) > 0 else "THERE ARE NO MATCHES", found
            if user_command[1].strip().lower() == "id":
                found = [self.book_searcher.by_id(user_command[2].strip())]
                return "SUCCESS." if len(found) > 0 else "THERE ARE NO MATCHES", found
        except Exception as e:
            raise RuntimeError(f"{e}")

    def edit(self, user_command: List[str]):
        try:
            if len(user_command) == 2:
                if self.book_editor.edit_status_only(user_command[1].strip()):
                    return "SUCCESSFULLY EDITED.", [self.book_searcher.by_id(user_command[1].strip())]
                else:
                    return "DATA WAS NOT FOUND", []

            elif len(user_command) == 6:
                if self.book_editor.edit(id=user_command[1].strip(),
                                         new_author=user_command[2].strip(),
                                         new_title=user_command[3].strip(),
                                         new_year=int(user_command[4].strip()),
                                         new_status=bool(user_command[5].strip())):
                    return "SUCCESSFULLY EDITED.", [self.book_searcher.by_id(user_command[1].strip())]
                else:
                    return "DATA WAS NOT FOUND", []
            else:
                return "ERROR. One(id) or five(id, author, title, year, status)" \
                       " parameters are requiered for editing an entry", []
        except Exception as e:
            raise RuntimeError(f"{e}")

    def delete(self, user_command: List[str]):
        try:
            if len(user_command) != 2:
                return "ERROR. ID parameter is requiered for deleting the entry.", []
            result, deleted_book = self.book_deleter.delete(user_command[1].strip())
            return "SUCCESSFULLY DELETED." if result else "ERROR. DATA NOT FOUND.", [deleted_book]
        except Exception as e:
            raise RuntimeError(f"{e}")

    def next_page(self):
        try:
            if self.page < float(self.book_searcher.get_total()) / float(self.to_show_on_page):
                self.page = self.page + 1
        except Exception as e:
            raise RuntimeError(f"{e}")

    def prev_page(self):
        try:
            if self.page >= 2:
                self.page = self.page - 1
        except Exception as e:
            raise RuntimeError(f"{e}")

    def change_table(self, user_command: List[str]):
        try:
            if len(user_command) == 2:
                self.to_show_on_page = int(user_command[1])
        except Exception as e:
            raise RuntimeError(f"{e}")
