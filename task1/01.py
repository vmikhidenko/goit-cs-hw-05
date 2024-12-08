import asyncio
import logging
from pathlib import Path
import shutil
from concurrent.futures import ThreadPoolExecutor

# Налаштування логування
logging.basicConfig(
    filename='file_sorter.log',  # Файл для запису логів
    level=logging.ERROR,          # Рівень логування - помилки
    format='%(asctime)s:%(levelname)s:%(message)s'  # Формат повідомлень
)

# Визначення фіксованих шляхів до вихідної та цільової папок
SOURCE_FOLDER = Path("/Users/volodymyrmikhidenko/Documents/Computer systems/goit-cs-hw-05/task1/source_folder")
DESTINATION_FOLDER = Path("/Users/volodymyrmikhidenko/Documents/Computer systems/goit-cs-hw-05/task1/destination_folder")

async def copy_file(file_path: Path, destination: Path, executor: ThreadPoolExecutor):
    """
    Асинхронно копіює файл у відповідну підпапку на основі розширення.

    Args:
        file_path (Path): Шлях до файлу, який потрібно скопіювати.
        destination (Path): Коренева директорія призначення.
        executor (ThreadPoolExecutor): Виконавець для запуску блокуючих операцій.
    """
    try:
        # Отримання розширення файлу або призначення 'no_extension', якщо відсутнє
        extension = file_path.suffix.lower().strip('.') or 'no_extension'
        target_dir = destination / extension
        # Створення підпапки для розширення, якщо її не існує
        target_dir.mkdir(parents=True, exist_ok=True)
        target_path = target_dir / file_path.name

        # Використання executor для блокуючої операції копіювання
        loop = asyncio.get_running_loop()
        await loop.run_in_executor(executor, shutil.copy2, str(file_path), str(target_path))
    except Exception as e:
        # Логування помилки
        logging.error(f"Помилка копіювання файлу {file_path} до {target_path}: {e}")

async def read_folder(source: Path, destination: Path, executor: ThreadPoolExecutor):
    """
    Рекурсивно читає всі файли з вихідної папки і створює задачі для їх копіювання.

    Args:
        source (Path): Вихідна директорія для читання файлів.
        destination (Path): Коренева директорія призначення.
        executor (ThreadPoolExecutor): Виконавець для запуску блокуючих операцій.
    """
    tasks = []
    try:
        # Обхід файлів у вихідній директорії
        for item in source.rglob('*'):  # Рекурсивно обходить усі файли та підкаталоги
            if item.is_file():  # Обробляються тільки файли
                task = asyncio.create_task(copy_file(item, destination, executor))
                tasks.append(task)
        # Очікування завершення всіх задач
        if tasks:
            await asyncio.gather(*tasks)
    except Exception as e:
        # Логування помилки
        logging.error(f"Помилка читання папки {source}: {e}")

async def main():
    """
    Основна асинхронна функція для виконання скрипту.
    """
    source = SOURCE_FOLDER
    destination = DESTINATION_FOLDER

    # Перевірка існування вихідної папки
    if not source.is_dir():
        logging.error(f"Вихідна папка не існує: {source}")
        print(f"Помилка: вихідна папка не існує: {source}")
        return

    # Створення цільової папки, якщо вона не існує
    destination.mkdir(parents=True, exist_ok=True)

    # Використання ThreadPoolExecutor для виконання блокуючих операцій
    executor = ThreadPoolExecutor(max_workers=10)

    # Асинхронна обробка файлів
    await read_folder(source, destination, executor)

    # Закриття пулу потоків
    executor.shutdown(wait=True)

if __name__ == "__main__":
    try:
        # Запуск основної асинхронної функції
        asyncio.run(main())
    except Exception as e:
        # Логування та вихід при несподіваній помилці
        logging.error(f"Несподівана помилка: {e}")
        print(f"Виникла несподівана помилка: {e}")
