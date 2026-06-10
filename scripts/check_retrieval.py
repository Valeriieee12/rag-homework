"""Скрипт для проверки работы поиска"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from app.retriever import Retriever


def main():
    print("🔍 Проверка системы поиска (Retrieval)\n")
    
    try:
        retriever = Retriever()
        print("✅ Ретривер инициализирован\n")
    except Exception as e:
        print(f"❌ Ошибка инициализации: {e}")
        return
    
    # Релевантные запросы
    good_queries = [
        "Что такое декоратор в Python?",
        "Чем отличается список от кортежа?",
        "lambda функция",
        "list comprehension",
        "асинхронное программирование",
    ]
    
    print("📝 Тест: Поиск по разным запросам:")
    for query in good_queries:
        results = retriever.retrieve(query, top_k=2)
        if results:
            print(f"\n   Запрос: '{query}'")
            for i, r in enumerate(results):
                print(f"      {i+1}. Score: {r['score']:.2f} | Doc: {r['doc_id']}")
                print(f"         Текст: {r['text'][:60]}...")


if __name__ == "__main__":
    main()