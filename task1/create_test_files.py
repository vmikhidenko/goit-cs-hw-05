import os
from pathlib import Path

def create_test_files(source_dir):
    """
    Створює тестові файли з різними розширеннями у вказаній папці.

    Args:
        source_dir (Path): Шлях до вихідної папки.
    """
    # Список файлів з різними розширеннями
    test_files = [
        "document1.txt",
        "document2.pdf",
        "image1.jpg",
        "image2.png",
        "script1.py",
        "script2.js",
        "archive1.zip",
        "archive2.tar.gz",
        "presentation1.pptx",
        "spreadsheet1.xlsx",
        "no_extension_file"
    ]

    # Створення файлів
    for file_name in test_files:
        file_path = source_dir / file_name
        # Створення батьківських директорій, якщо необхідно
        file_path.parent.mkdir(parents=True, exist_ok=True)
        # Створення файлу з простим вмістом
        with open(file_path, 'w') as f:
            f.write(f"Це тестовий файл: {file_name}")

    print(f"Тестові файли створено у папці: {source_dir}")

if __name__ == "__main__":
    # Визначте шлях до вихідної папки
    source_folder = Path("source_folder")  # Ви можете змінити цей шлях за потребою

    # Створення вихідної папки, якщо вона не існує
    source_folder.mkdir(parents=True, exist_ok=True)

    # Виклик функції для створення тестових файлів
    create_test_files(source_folder)
