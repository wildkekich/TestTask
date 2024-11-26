import os
from src.domain.models.BookDatabase import BookDatabase
from src.views.ConsoleView import ConsoleView
from src.domain.controllers.ConsoleController import ConsoleController
from src.domain.controllers.BookCreator import BookCreator
from src.domain.controllers.BookDeleter import BookDeleter
from src.domain.controllers.BookEditor import BookEditor
from src.domain.controllers.BookSearcher import BookSearcher

other_folder_path = os.path.join(os.path.dirname(__file__), "other")
db_file_path = os.path.join(other_folder_path, "database.json")


if __name__ == "__main__":
    os.makedirs(other_folder_path, exist_ok=True)
    if not os.path.exists(db_file_path):
        with open(db_file_path, "w") as file:
            file.write("[]")

    book_db = BookDatabase(db_file_path)
    book_creator = BookCreator(book_db)
    book_deleter = BookDeleter(book_db)
    book_searcher = BookSearcher(book_db)
    book_editor = BookEditor(book_db)
    console_view = ConsoleView()
    console_controller = ConsoleController(book_searcher, book_creator, book_deleter, book_editor, console_view)

    console_controller.main()

    exit()
