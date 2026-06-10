"""Модуль для поиска релевантных чанков"""

import sys
from pathlib import Path
from typing import List, Dict

sys.path.insert(0, str(Path(__file__).parent.parent))

import chromadb
from sentence_transformers import SentenceTransformer
from app.config import DATA_INDEX_DIR, TOP_K


class Retriever:
    """Класс для поиска по векторному индексу"""
    
    def __init__(self):
        """Инициализация ретривера"""
        self.chroma_path = DATA_INDEX_DIR / "chroma_db"
        
        if not self.chroma_path.exists():
            raise FileNotFoundError(
                f"Индекс не найден в {self.chroma_path}. "
                "Запусти: uv run python scripts/build_index.py"
            )
        
        # Подключаемся к ChromaDB
        self.client = chromadb.PersistentClient(path=str(self.chroma_path))
        self.collection = self.client.get_collection("rag_docs")
        
        # Загружаем модель для эмбеддингов
        print("🔄 Загрузка модели для поиска...")
        self.model = SentenceTransformer('intfloat/multilingual-e5-small')
        print("✅ Модель загружена")
    
    def retrieve(self, query: str, top_k: int = TOP_K) -> List[Dict]:
        """
        Поиск релевантных чанков по запросу
        
        Args:
            query: текст запроса
            top_k: количество результатов
        
        Returns:
            список чанков с метаданными
        """
        # Создаем эмбеддинг запроса
        query_embedding = self.model.encode([query])
        
        # Ищем в коллекции
        results = self.collection.query(
            query_embeddings=query_embedding.tolist(),
            n_results=top_k
        )
        
        # Форматируем результаты
        retrieved_chunks = []
        for i in range(len(results['documents'][0])):
            retrieved_chunks.append({
                'chunk_id': results['ids'][0][i],
                'doc_id': results['metadatas'][0][i]['doc_id'],
                'text': results['documents'][0][i],
                'score': 1.0 - (i * 0.1),  # Чем выше в списке, тем выше score
                'metadata': {
                    'title': results['metadatas'][0][i].get('title', ''),
                    'source': results['metadatas'][0][i].get('source', ''),
                    'chunk_index': results['metadatas'][0][i].get('chunk_index', 0)
                }
            })
        
        return retrieved_chunks


# Для тестирования
if __name__ == "__main__":
    print("🔍 Тестирование поиска...")
    
    retriever = Retriever()
    
    test_queries = [
        "Что такое декоратор в Python?",
        "Чем отличается list от tuple?",
    ]
    
    for query in test_queries:
        print(f"\n📝 Запрос: {query}")
        results = retriever.retrieve(query, top_k=3)
        
        for i, result in enumerate(results):
            print(f"   {i+1}. Score: {result['score']:.2f}")
            print(f"      Doc ID: {result['doc_id']}")
            print(f"      Text: {result['text'][:80]}...")