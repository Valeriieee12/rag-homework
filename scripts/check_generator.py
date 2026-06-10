"""Скрипт для проверки генератора ответов"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from app.generator import Generator


def main():
    print("🤖 Проверка генератора ответов\n")
    
    generator = Generator()
    
    print("=" * 60)
    
    # Тест 1: Вопрос по Python
    query1 = "Что такое декоратор в Python?"
    print(f"\n📝 Тест 1 (должен ответить): {query1}")
    print("-" * 50)
    result1 = generator.generate(query1)
    print(f"📖 Ответ: {result1['answer'][:400]}")
    print(f"📚 Источников: {len(result1['sources'])}")
    
    print("\n" + "=" * 60)
    
    # Тест 2: Еще вопрос по Python
    query2 = "Чем отличается list от tuple?"
    print(f"\n📝 Тест 2 (должен ответить): {query2}")
    print("-" * 50)
    result2 = generator.generate(query2)
    print(f"📖 Ответ: {result2['answer'][:400]}")
    print(f"📚 Источников: {len(result2['sources'])}")
    
    print("\n" + "=" * 60)
    
    # Тест 3: Вопрос не по теме (должен отказаться)
    query3 = "Как приготовить шоколадный торт?"
    print(f"\n📝 Тест 3 (должен отказаться): {query3}")
    print("-" * 50)
    result3 = generator.generate(query3)
    print(f"📖 Ответ: {result3['answer']}")
    
    print("\n" + "=" * 60)
    print("\n✅ Проверка завершена!")


if __name__ == "__main__":
    main()