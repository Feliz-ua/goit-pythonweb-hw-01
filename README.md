# goit-pythonweb-hw-01

Навчальний Python-проєкт із двома завданнями: реалізація патерна Factory та системи керування бібліотекою за принципами SOLID.

## Структура проєкту

```text
goit-pythonweb-hw-01/
├── main.py
├── README.md
└── src/
    ├── task1.py
    ├── task2.py
    ├── book.py
    ├── task2_storage.py
    └── task2_storage/
        └── book.json
```

## Встановлення

### Poetry

```bash
poetry install
poetry add colorama
```

## Запуск

```bash
python main.py
```

Після запуску відкривається меню вибору:

```text
1. Task 1 - Патерн фабрика
2. Task 2 - SOLID
0. Вихід
```

## Task 1

У `task1.py` реалізовано патерн **Factory** для створення транспортних засобів з різними регіональними специфікаціями:

- `Vehicle`
- `Car`
- `Motorcycle`
- `VehicleFactory`
- `USVehicleFactory`
- `EUVehicleFactory`

## Task 2

У `task2.py` реалізовано систему керування бібліотекою книг із дотриманням принципів **SOLID**.

Основні можливості:

- додавання книги
- видалення книги
- перегляд списку книг
- збереження книг у JSON-файлі
- завантаження книг при повторному запуску

Файл із даними:

```text
src/task2_storage/book.json
```

## Особливості

- використовується типізація
- службові повідомлення виводяться через `logging`
- код форматують за допомогою `black`
- у Task 2 використовується `Colorama` для кольорового виводу книг у консолі

## Форматування коду

```bash
black .
```
