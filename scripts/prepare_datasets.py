"""Скрипт для создания демо-датасета с вопросами и ответами по Python"""

import json
import random
from pathlib import Path

# Данные: вопросы и ответы по Python (1000+ записей)
python_qa = []

# Базовые вопросы и ответы по Python
topics = [
    {
        "question": "Что такое декоратор в Python?",
        "answer": "Декоратор — это функция, которая принимает другую функцию и расширяет её поведение без явного изменения. Используется синтаксис @decorator."
    },
    {
        "question": "Чем отличается list от tuple?",
        "answer": "List изменяемый (mutable), tuple неизменяемый (immutable). List создается через [] или list(), tuple через () или tuple()."
    },
    {
        "question": "Что такое lambda функция?",
        "answer": "Lambda — это анонимная функция в одну строку. Синтаксис: lambda arguments: expression. Пример: square = lambda x: x**2"
    },
    {
        "question": "Как работает метод .append()?",
        "answer": ".append() добавляет один элемент в конец списка. Пример: my_list.append(5) добавит число 5 в конец списка."
    },
    {
        "question": "Что такое list comprehension?",
        "answer": "List comprehension — это способ создания списков в одну строку. Пример: squares = [x**2 for x in range(10)]"
    },
    {
        "question": "Что такое словарь (dict) в Python?",
        "answer": "Словарь — это коллекция пар ключ-значение. Создается через {} или dict(). Ключи должны быть неизменяемыми (строки, числа, кортежи)."
    },
    {
        "question": "Что делает оператор 'is' в Python?",
        "answer": "Оператор 'is' сравнивает, являются ли два объекта одним и тем же объектом в памяти (идентичность), а не равенство значений."
    },
    {
        "question": "Как создать класс в Python?",
        "answer": "Класс создается через ключевое слово 'class'. Пример: class MyClass: pass. Методы класса получают self как первый параметр."
    },
    {
        "question": "Что такое наследование в Python?",
        "answer": "Наследование позволяет классу унаследовать атрибуты и методы от другого класса. Синтаксис: class Child(Parent): pass"
    },
    {
        "question": "Что делает метод .join() для строк?",
        "answer": ".join() объединяет элементы списка в одну строку с разделителем. Пример: ', '.join(['a', 'b', 'c']) вернет 'a, b, c'"
    },
    {
        "question": "Как обработать исключение в Python?",
        "answer": "Исключения обрабатываются через блок try/except. Пример: try: x = 1/0 except ZeroDivisionError: print('Ошибка')"
    },
    {
        "question": "Что такое генераторы (yield) в Python?",
        "answer": "Генераторы — это функции, которые используют yield вместо return. Они возвращают значения по одному и сохраняют состояние между вызовами."
    },
    {
        "question": "Как прочитать файл в Python?",
        "answer": "Файл читается через функцию open(). Пример: with open('file.txt', 'r') as f: content = f.read()"
    },
    {
        "question": "Что такое with statement в Python?",
        "answer": "with используется для автоматического управления ресурсами. Гарантирует закрытие файла или освобождение ресурса даже при ошибках."
    },
    {
        "question": "Как создать модуль в Python?",
        "answer": "Модуль — это просто файл с расширением .py. Импортируется через import имя_файла. Функции и классы доступны после импорта."
    },
]

# Размножаем записи, чтобы получить 1000+ вариантов
# Генерируем вариации вопросов с разными формулировками
variations = [
    "Пожалуйста, объясни, {}",
    "Что означает {} в Python?",
    "Расскажи о {}",
    "Как работает {}?",
    "Что такое {} простыми словами?",
    "Объясни новичку, что такое {}",
    "Зачем нужен {} в программировании?",
    "{} в Python - как использовать?",
    "Чем полезен {}?",
    "Подробно про {}"
]

for i in range(120):  # Создаем ~120 вариаций для 15 тем = ~1800 записей
    for topic in topics:
        variation_template = random.choice(variations)
        question = variation_template.format(topic["question"])
        
        # Добавляем разные примеры к ответам
        extra_example = random.choice([
            "", ". Пример кода можно найти в документации.", 
            " Это одна из базовых концепций Python.",
            " Используйте это в своем коде.",
            " Рекомендуется для написания качественного кода."
        ])
        
        answer = topic["answer"] + extra_example
        
        python_qa.append({
            "id": f"python_doc_{len(python_qa):04d}",
            "title": topic["question"][:50],
            "text": f"Вопрос: {question}\nОтвет: {answer}",
            "source": "Python Tutorial Demo"
        })

# Добавляем еще 500 случайных фактов о Python
python_tips = [
    "Python поддерживает множественное присваивание: a, b = 1, 2",
    "В Python есть встроенная функция enumerate() для итерации по индексам",
    "PEP 8 — это руководство по стилю кода в Python",
    "Функция zip() объединяет несколько итерируемых объектов",
    "Метод .split() разделяет строку на список подстрок",
    "Python использует динамическую типизацию",
    "В Python есть list, tuple, set, dict — основные структуры данных",
    "pip — это менеджер пакетов для Python",
    "virtualenv создает изолированные окружения для Python",
    "f-строки позволяют вставлять переменные прямо в строки: f'Hello {name}'",
]

for i in range(500):
    tip = random.choice(python_tips)
    python_qa.append({
        "id": f"python_tip_{len(python_qa):04d}",
        "title": f"Совет по Python #{i}",
        "text": f"Совет: {tip}",
        "source": "Python Tips Demo"
    })

# Создаем структуру для datasets.json
datasets = {
    "datasets": python_qa
}

# Сохраняем в файл
output_path = Path("data/raw/datasets.json")
output_path.parent.mkdir(parents=True, exist_ok=True)

with open(output_path, "w", encoding="utf-8") as f:
    json.dump(datasets, f, ensure_ascii=False, indent=2)

print(f"✅ Создан датасет с {len(python_qa)} записями")
print(f"   Файл сохранен: {output_path}")