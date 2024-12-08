import requests
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
import matplotlib.pyplot as plt
import re


def fetch_text(url):
    """
    Завантажує текст за URL-адресою.

    Args:
        url (str): URL-адреса текстового файлу.

    Returns:
        str: Зміст тексту.
    """
    response = requests.get(url)
    response.raise_for_status()  # Перевірка статусу відповіді
    return response.text


def map_reduce(text, workers=4):
    """
    Аналізує частоту слів у тексті за допомогою MapReduce.

    Args:
        text (str): Текст для аналізу.
        workers (int): Кількість потоків для обробки.

    Returns:
        Counter: Об'єкт Counter з частотою слів.
    """
    # Очищення тексту і розбиття на слова
    words = re.findall(r'\b\w+\b', text.lower())

    # Розбиття списку слів на частини для потоків
    chunk_size = len(words) // workers
    chunks = [words[i:i + chunk_size] for i in range(0, len(words), chunk_size)]

    # Map функція: підрахунок частоти слів у кожному блоці
    def count_words(chunk):
        return Counter(chunk)

    # Виконання в потоках
    with ThreadPoolExecutor(max_workers=workers) as executor:
        results = executor.map(count_words, chunks)

    # Reduce функція: об'єднання результатів
    total_counts = Counter()
    for result in results:
        total_counts.update(result)

    return total_counts


def visualize_top_words(counter, top_n=10):
    """
    Візуалізує топ-слова за частотою використання.

    Args:
        counter (Counter): Частота слів.
        top_n (int): Кількість слів для відображення.
    """
    top_words = counter.most_common(top_n)
    words, counts = zip(*top_words)

    plt.barh(words, counts, color='skyblue')
    plt.xlabel('Frequency')
    plt.ylabel('Words')
    plt.title('Top 10 Most Frequent Words')
    plt.gca().invert_yaxis()  # Інверсія осі Y для кращого вигляду
    plt.show()


if __name__ == "__main__":
    # URL текстового файлу
    url = "https://www.gutenberg.org/files/1342/1342-0.txt"  # Замініть на потрібну URL-адресу

    try:
        # Завантаження тексту
        print("Завантаження тексту...")
        text = fetch_text(url)

        # Аналіз частоти слів
        print("Аналіз частоти слів...")
        word_counts = map_reduce(text)

        # Візуалізація результатів
        print("Візуалізація результатів...")
        visualize_top_words(word_counts)

    except Exception as e:
        print(f"Виникла помилка: {e}")
