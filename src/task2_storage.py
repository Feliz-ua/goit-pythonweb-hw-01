# Модуль для збереження та завантаження книг у JSON-файлі

import json
from pathlib import Path
from typing import List
from src.book import Book


class JsonBookStorage:
    # Збереження книг у JSON-файлі

    def __init__(self, file_path: Path) -> None:
        self._file_path = file_path
        self._ensure_file_exists()

    def load_books(self) -> List[Book]:
        # Завантаження списку книг із JSON-файлу
        with self._file_path.open("r", encoding="utf-8") as file:
            data = json.load(file)

        return [
            Book(
                title=item["title"],
                author=item["author"],
                year=item["year"],
            )
            for item in data
        ]

    def save_books(self, books: List[Book]) -> None:
        # Зберігання списку книг у JSON-файл.
        data = [
            {
                "title": book.title,
                "author": book.author,
                "year": book.year,
            }
            for book in books
        ]

        with self._file_path.open("w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

    def _ensure_file_exists(self) -> None:
        self._file_path.parent.mkdir(parents=True, exist_ok=True)
        if not self._file_path.exists():
            self._file_path.write_text("[]", encoding="utf-8")
