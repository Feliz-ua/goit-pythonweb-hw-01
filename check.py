"""Скрипт для аналізу імпортів у Python-проєкті та пошуку відсутніх залежностей у pyproject.toml."""

from __future__ import annotations

import ast
import sys
from pathlib import Path
from typing import Iterable

try:
    import tomllib
except ModuleNotFoundError:
    print("Цей скрипт потребує Python 3.11+ для роботи з tomllib.")
    sys.exit(1)


PROJECT_ROOT = Path(__file__).resolve().parent
PYPROJECT_PATH = PROJECT_ROOT / "pyproject.toml"
EXCLUDED_DIRS = {".venv", "venv", "__pycache__", ".git", ".idea", ".mypy_cache", ".pytest_cache"}
IGNORED_IMPORTS = {"src"}

PACKAGE_NAME_MAP = {
    "bs4": "beautifulsoup4",
    "cv2": "opencv-python",
    "dotenv": "python-dotenv",
    "PIL": "pillow",
    "sklearn": "scikit-learn",
    "yaml": "pyyaml",
}


def iter_python_files(root: Path) -> Iterable[Path]:
    """Повертає всі Python-файли проєкту."""
    for path in root.rglob("*.py"):
        if any(part in EXCLUDED_DIRS for part in path.parts):
            continue
        yield path


def collect_local_modules(root: Path) -> set[str]:
    """Збирає назви локальних модулів і пакетів проєкту."""
    local_modules: set[str] = {"src"}

    for path in iter_python_files(root):
        local_modules.add(path.stem)

    for path in root.rglob("*"):
        if path.is_dir() and (path / "__init__.py").exists():
            local_modules.add(path.name)

    return local_modules


def extract_imports(file_path: Path) -> set[str]:
    """Витягує верхньорівневі назви імпортів із Python-файлу."""
    imports: set[str] = set()
    source = file_path.read_text(encoding="utf-8")
    tree = ast.parse(source, filename=str(file_path))

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imports.add(alias.name.split(".")[0])
        elif isinstance(node, ast.ImportFrom):
            if node.module and node.level == 0:
                imports.add(node.module.split(".")[0])

    return imports


def get_declared_dependencies(pyproject_path: Path) -> set[str]:
    """Повертає залежності, вже оголошені у pyproject.toml."""
    if not pyproject_path.exists():
        return set()

    data = tomllib.loads(pyproject_path.read_text(encoding="utf-8"))
    declared: set[str] = set()

    project_deps = data.get("project", {}).get("dependencies", [])
    for dep in project_deps:
        name = dep.split(";")[0].strip().split(" ")[0].split("[")[0]
        declared.add(name.lower())

    poetry_deps = data.get("tool", {}).get("poetry", {}).get("dependencies", {})
    for name in poetry_deps:
        if name.lower() != "python":
            declared.add(name.lower())

    return declared


def normalize_package_name(import_name: str) -> str:
    """Нормалізує назву імпорту до ймовірної назви пакета."""
    return PACKAGE_NAME_MAP.get(import_name, import_name).lower()


def is_stdlib_module(module_name: str) -> bool:
    """Перевіряє, чи належить модуль до стандартної бібліотеки."""
    if module_name in sys.builtin_module_names:
        return True

    if hasattr(sys, "stdlib_module_names"):
        return module_name in sys.stdlib_module_names

    return False


def main() -> None:
    """Аналізує імпорти та показує відсутні залежності."""
    local_modules = collect_local_modules(PROJECT_ROOT)
    declared_dependencies = get_declared_dependencies(PYPROJECT_PATH)

    found_imports: set[str] = set()
    for file_path in iter_python_files(PROJECT_ROOT):
        found_imports.update(extract_imports(file_path))

    external_candidates: set[str] = set()
    for import_name in found_imports:
        if import_name in IGNORED_IMPORTS:
            continue
        if import_name in local_modules:
            continue
        if is_stdlib_module(import_name):
            continue
        external_candidates.add(normalize_package_name(import_name))

    missing_dependencies = sorted(external_candidates - declared_dependencies)

    print("=== Аналіз залежностей ===")
    print(f"Знайдено імпорти: {len(found_imports)}")
    print(f"Локальні модулі: {len(local_modules)}")
    print(f"Оголошені залежності: {len(declared_dependencies)}")
    print()

    if not missing_dependencies:
        print("Усі знайдені зовнішні залежності вже є в pyproject.toml.")
        return

    print("Можливо відсутні залежності:")
    for dependency in missing_dependencies:
        print(f"- {dependency}")

    print()
    print("Команди для додавання через Poetry:")
    for dependency in missing_dependencies:
        print(f"poetry add {dependency}")


if __name__ == "__main__":
    main()
