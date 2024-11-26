from src.domain.models.Book import Book
from typing import List
import os


class ConsoleView:
    def show(self, books: List[Book], page: int):
        headers = ["ID", "Author", "Title", "Year", "Status"]
        column_widths = [
            max(len(str(getattr(book, attr.lower(), ""))) for book in books + [headers])
            for attr in headers
        ]
        row_format = " | ".join(f"{{:<{w}}}" for w in column_widths)
        print(f"Page:{page}")
        print(row_format.format(*headers))
        print("-" * (sum(column_widths) + 3 * (len(headers) - 1)))
        for book in books:
            if (isinstance(book, Book)):
                print(row_format.format(book.id, book.author, book.title, book.year, "In stock" if book.status else "Out of stock"))

    def react_to_user_interaction(self, message: str, books: List[Book]):
        self.clear_console()
        to_show = f"{message}\n"
        for book in books:
            if(isinstance(book, Book)):
                to_show += f"{book.id} {book.year} {book.author} {book.title} {'In stock' if book.status else 'Out of stock'}\n"
        print(to_show)

    def show_menu(self):
        self.clear_console()
        menu = """
i/if - insert/insert file - (author; title; year) or path to the JSON-file Ex: \"i; Pushkin A.S.; Evgeniy Onegin; 1833\"
s - search - by [author/title/year] (string) Ex: \"s; author; Pushkin A.S.; \"
e - edit - id(string) Ex: \"e 0x34f0\"
d - delete - id(string) Ex: \"d 0x34f0\"
> - next page
< - previous page
c - change table's showing items - num(int) Ex: \"c 20\"
exit - exit
"""
        print(menu)

    def clear_console(self):
        os.system('cls' if os.name == 'nt' else 'clear')
