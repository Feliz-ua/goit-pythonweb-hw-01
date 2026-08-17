import logging

from src.task1 import demo_factories as task1
from src.task2 import main as task2

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


def show_menu() -> None:
    """Відображає меню вибору завдання."""
    print("\nОберіть завдання для запуску:")
    print("1. Task 1 - Патерн фабрика")
    print("2. Task 2 - SOLID")
    print("0. Вихід")


def run_task(choice: str) -> bool:
    """Запускає вибране завдання."""
    match choice:
        case "1":
            logger.info("Запуск Task 1")
            task1()
            return True
        case "2":
            logger.info("Запуск Task 2")
            task2()
            return True
        case "0":
            logger.info("Завершення роботи програми")
            return False
        case _:
            logger.info("Невірний вибір. Спробуйте ще раз.")
            return True


def main() -> None:
    # Запускає головне меню програми.
    logger.info("Запуск головного меню")

    is_running = True
    while is_running:
        show_menu()
        choice = input("Введіть номер опції: ").strip()
        is_running = run_task(choice)


if __name__ == "__main__":
    main()
