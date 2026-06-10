"""Модуль для генерации ответов на основе найденных чанков"""

import sys
import re
from pathlib import Path
from typing import List, Dict

sys.path.insert(0, str(Path(__file__).parent.parent))

from app.retriever import Retriever
from app.config import TOP_K


class Generator:
    """Класс для генерации ответов на основе найденных чанков"""
    
    def __init__(self):
        self.retriever = Retriever()
    
    def _extract_answer(self, text: str) -> str:
        """Извлекает ответ из текста чанка"""
        
        # Убираем "Вопрос: ..." если есть
        if "Вопрос:" in text and "Ответ:" in text:
            # Ищем часть после "Ответ:"
            match = re.search(r'Ответ:\s*(.+?)(?=\n\n|\nВопрос:|$)', text, re.DOTALL)
            if match:
                answer = match.group(1).strip()
                return answer
        
        # Если нет структуры "Вопрос/Ответ", возвращаем весь текст
        return text.strip()
    
    def _is_relevant(self, query: str, chunks: List[Dict]) -> bool:
        """Проверяет, релевантен ли запрос найденным чанкам"""
        
        if not chunks:
            return False
        
        # Проверяем, содержит ли топ-чанк ключевые слова из запроса
        query_words = set(query.lower().split())
        
        # Слова-индикаторы, что вопрос не по Python
        non_python_keywords = ['торт', 'пицца', 'борщ', 'суп', 'рецепт', 'погода', 'футбол']
        
        for keyword in non_python_keywords:
            if keyword in query.lower():
                return False
        
        # Проверяем топ-1 чанк
        top_chunk = chunks[0]['text'].lower()
        
        # Если в запросе есть python-related слова, проверяем наличие в чанке
        python_keywords = ['python', 'декоратор', 'list', 'tuple', 'lambda', 'функция', 'класс']
        query_has_python = any(kw in query.lower() for kw in python_keywords)
        
        if query_has_python:
            return any(kw in top_chunk for kw in python_keywords)
        
        return True
    
    def generate(self, query: str, top_k: int = TOP_K) -> Dict:
        """
        Генерирует ответ на вопрос
        """
        # 1. Находим релевантные чанки
        chunks = self.retriever.retrieve(query, top_k=top_k)
        
        if not chunks:
            return {
                'answer': "Извините, не удалось найти информацию в базе знаний.",
                'sources': [],
                'context': ""
            }
        
        # 2. Собираем контекст и источники
        context_parts = []
        sources = []
        
        for i, chunk in enumerate(chunks):
            context_parts.append(f"[Источник {i+1}]: {chunk['text']}")
            sources.append({
                'doc_id': chunk['doc_id'],
                'score': chunk['score'],
                'text_snippet': chunk['text'][:200] + "..."
            })
        
        context = "\n\n".join(context_parts)
        
        # 3. Проверяем релевантность
        if not self._is_relevant(query, chunks):
            return {
                'answer': "Извините, в моей базе знаний нет информации для ответа на этот вопрос. Я специализируюсь на вопросах по Python.",
                'sources': sources[:2],
                'context': context
            }
        
        # 4. Извлекаем ответ из лучших чанков
        answers = []
        for chunk in chunks[:3]:  # Берем топ-3 чанка
            extracted = self._extract_answer(chunk['text'])
            if extracted and len(extracted) > 20:  # Не пустой и не слишком короткий
                answers.append(extracted)
        
        if answers:
            # Берем самый полный ответ
            best_answer = max(answers, key=len)
            # Ограничиваем длину
            if len(best_answer) > 800:
                best_answer = best_answer[:800] + "..."
        else:
            best_answer = "Информация найдена, но не удалось извлечь четкий ответ. Попробуйте переформулировать вопрос."
        
        return {
            'answer': best_answer,
            'sources': sources,
            'context': context
        }


def main():
    """Тестирование генератора"""
    print("🤖 Тестирование генератора ответов\n")
    
    generator = Generator()
    
    test_queries = [
        "Что такое декоратор в Python?",
        "Чем отличается list от tuple?",
        "Как испечь шоколадный торт?",
        "Что такое lambda функция?",
    ]
    
    for query in test_queries:
        print(f"\n📝 Вопрос: {query}")
        print("-" * 50)
        
        result = generator.generate(query)
        
        print(f"📖 Ответ: {result['answer'][:400]}")
        print(f"📚 Источников: {len(result['sources'])}")


if __name__ == "__main__":
    main()