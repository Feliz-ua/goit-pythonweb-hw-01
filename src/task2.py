import logging
from abc import ABC, abstractmethod
from pathlib import Path
from typing import List, Optional

from colorama import Fore, Style, init

from src.book import Book
from src.task2_storage import JsonBookStorage

logger = logging.getLogger(__name__)


class LibraryInterface(ABC):
    # Інтерфейс для реалізацій бібліотеки.

    @abstractmethod
    def add_book(self, book: Book) -> None:
        # Додає книгу до бібліотеки
        pass

    @abstractmethod
    def remove_book(self, title: str) -> bool:
        # Видаляє книгу за назвою.
        pass

    @abstractmethod
    def get_books(self) -> List[Book]:
        # Повертає всі книги бібліотеки.
        pass


class Library(LibraryInterface):
    # Реалізація бібліотеки

    def __init__(self, storage: JsonBookStorage) -> None:
        self._storage = storage
        self._books: List[Book] = self._storage.load_books()
        logger.info("Завантажено %s книг із файлу", len(self._books))

    def add_book(self, book: Book) -> None:
        self._books.append(book)
        self._storage.save_books(self._books)
        logger.info("Книгу '%s' додано до бібліотеки", book.title)

    def remove_book(self, title: str) -> bool:
        for book in self._books:
            if book.title.lower() == title.lower():
                self._books.remove(book)
                self._storage.save_books(self._books)
                logger.info("Книгу '%s' видалено з бібліотеки", book.title)
                return True

        logger.info("Книгу з назвою '%s' не знайдено", title)
        return False

    def get_books(self) -> List[Book]:
        return self._books.copy()


class LibraryManager:
    # Менеджер верхнього рівня, що працює з абстракцією бібліотеки

    def __init__(self, library: LibraryInterface) -> None:
        self._library = library

    def add_book(self, title: str, author: str, year: str) -> None:
        parsed_year = self._parse_year(year)
        if parsed_year is None:
            logger.info("Некоректний рік видання: %s", year)
            return

        book = Book(title=title, author=author, year=parsed_year)
        self._library.add_book(book)

    def remove_book(self, title: str) -> None:
        self._library.remove_book(title)

    def show_books(self) -> None:
        books = self._library.get_books()
        if not books:
            logger.info("Бібліотека порожня")
            return

        for book in books:
            colored_message = (
                f"Назва: {Fore.YELLOW}{book.title}{Style.RESET_ALL}, "
                f"Автор: {Fore.GREEN}{book.author}{Style.RESET_ALL}, "
                f"Рік: {Fore.MAGENTA}{book.year}{Style.RESET_ALL}"
            )
            logger.info(colored_message)

    @staticmethod
    def _parse_year(year: str) -> Optional[int]:
        # Перетворює рядок року на ціле число.
        try:
            return int(year)
        except ValueError:
            return None


def main() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )
    init(autoreset=True)
    storage_path = Path("src") / "task2_storage" / "book.json"
    storage = JsonBookStorage(storage_path)
    library: LibraryInterface = Library(storage)
    manager = LibraryManager(library)

    while True:
        command = input("Введіть команду (add, remove, show, exit): ").strip().lower()

        match command:
            case "add":
                title = input("Введіть назву книги: ").strip()
                author = input("Введіть автора книги: ").strip()
                year = input("Введіть рік видання книги: ").strip()
                manager.add_book(title, author, year)
            case "remove":
                title = input("Введіть назву книги для видалення: ").strip()
                manager.remove_book(title)
            case "show":
                manager.show_books()
            case "exit":
                logger.info("Завершення роботи програми")
                break
            case _:
                logger.info("Невідома команда. Спробуйте ще раз.")


if __name__ == "__main__":
    main()
