"""Скрипт для создания векторного индекса из чанков"""

import sys
import json
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import chromadb
from sentence_transformers import SentenceTransformer
from app.config import DATA_PROCESSED_DIR, DATA_INDEX_DIR, CHUNK_SIZE

def main():
    """Загружает чанки и создает индекс в ChromaDB"""
    
    # Пути
    chunks_path = DATA_PROCESSED_DIR / "chunks.jsonl"
    chroma_db_path = DATA_INDEX_DIR / "chroma_db"
    
    # Проверяем, что файл с чанками существует
    if not chunks_path.exists():
        print(f"❌ Ошибка: файл {chunks_path} не найден")
        print("   Сначала запусти: uv run python app/chunker.py")
        return
    
    # Загружаем чанки
    chunks = []
    with open(chunks_path, 'r', encoding='utf-8') as f:
        for line in f:
            if line.strip():
                chunks.append(json.loads(line))
    
    print(f"📚 Загружено {len(chunks)} чанков")
    
    # Загружаем модель для эмбеддингов
    print("🔄 Загрузка модели эмбеддингов...")
    model = SentenceTransformer('intfloat/multilingual-e5-small')
    print("✅ Модель загружена")
    
    # Создаем эмбеддинги для всех чанков
    print(f"🔄 Создание эмбеддингов для {len(chunks)} чанков...")
    texts = [chunk['text'] for chunk in chunks]
    
    # Обрабатываем батчами для экономии памяти
    batch_size = 32
    all_embeddings = []
    
    for i in range(0, len(texts), batch_size):
        batch = texts[i:i+batch_size]
        batch_embeddings = model.encode(batch)
        all_embeddings.extend(batch_embeddings)
        print(f"   Прогресс: {min(i+batch_size, len(texts))}/{len(texts)}")
    
    print("✅ Эмбеддинги созданы")
    
    # Создаем или очищаем коллекцию в ChromaDB
    print("🔄 Создание индекса в ChromaDB...")
    
    # Удаляем старую базу если есть
    import shutil
    if chroma_db_path.exists():
        shutil.rmtree(chroma_db_path)
        print("   Старый индекс удален")
    
    # Создаем новый клиент
    client = chromadb.PersistentClient(path=str(chroma_db_path))
    
    # Создаем коллекцию
    collection = client.create_collection(
        name="rag_docs",
        metadata={"hnsw:space": "cosine"}
    )
    
    # Добавляем чанки в коллекцию
    batch_size = 100
    for i in range(0, len(chunks), batch_size):
        batch_chunks = chunks[i:i+batch_size]
        batch_embeddings = all_embeddings[i:i+batch_size]
        
        collection.add(
            ids=[chunk['chunk_id'] for chunk in batch_chunks],
            embeddings=[emb.tolist() for emb in batch_embeddings],
            documents=[chunk['text'] for chunk in batch_chunks],
            metadatas=[{
                'doc_id': chunk['doc_id'],
                'chunk_index': chunk['metadata'].get('chunk_index', 0),
                'source': chunk['metadata'].get('source', ''),
                'title': chunk['metadata'].get('title', '')
            } for chunk in batch_chunks]
        )
        
        print(f"   Добавлено {min(i+batch_size, len(chunks))}/{len(chunks)} чанков")
    
    print(f"✅ Индекс создан! Всего {collection.count()} векторов")
    print(f"   База сохранена в: {chroma_db_path}")
    
    # Проверка поиска
    print("\n🔍 Тест поиска:")
    test_query = "Что такое декоратор?"
    test_embedding = model.encode([test_query])
    results = collection.query(
        query_embeddings=test_embedding.tolist(),
        n_results=3
    )
    
    print(f"   Запрос: '{test_query}'")
    print(f"   Найдено {len(results['documents'][0])} результатов:")
    for i, doc in enumerate(results['documents'][0]):
        print(f"   {i+1}. {doc[:100]}...")
        print(f"      (doc_id: {results['metadatas'][0][i]['doc_id']})")

if __name__ == "__main__":
    main()