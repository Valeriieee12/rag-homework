"""Модуль для нарезки документов на чанки"""

import json
from pathlib import Path
from typing import List, Dict
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))

from app.config import CHUNK_SIZE, CHUNK_OVERLAP, DATA_PROCESSED_DIR

try:
    from langchain_text_splitters import RecursiveCharacterTextSplitter
    print("✅ LangChain импортирован успешно")
except ImportError:
    print("❌ LangChain не установлен. Установи: uv add langchain-text-splitters")
    raise


def chunk_documents(input_path: Path, output_path: Path, chunk_size: int = CHUNK_SIZE, overlap: int = CHUNK_OVERLAP) -> int:
    """
    Нарезает документы на чанки
    
    Args:
        input_path: путь к documents.jsonl
        output_path: путь для сохранения chunks.jsonl
        chunk_size: размер чанка в символах
        overlap: перекрытие между чанками
    
    Returns:
        количество созданных чанков
    """
    
    # Инициализируем сплиттер
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=overlap,
        separators=["\n\n", "\n", ". ", " ", ""],
        length_function=len,
    )
    
    chunks = []
    
    # Читаем документы
    with open(input_path, 'r', encoding='utf-8') as f:
        for line in f:
            if line.strip():
                doc = json.loads(line)
                
                # Разбиваем текст на чанки
                doc_chunks = text_splitter.split_text(doc['text'])
                
                # Создаем записи для каждого чанка
                for i, chunk_text in enumerate(doc_chunks):
                    chunk = {
                        "chunk_id": f"{doc['doc_id']}_chunk_{i}",
                        "doc_id": doc['doc_id'],
                        "text": chunk_text,
                        "metadata": {
                            "title": doc['metadata'].get('title', ''),
                            "source": doc['metadata'].get('source', ''),
                            "chunk_index": i
                        }
                    }
                    chunks.append(chunk)
    
    # Сохраняем чанки
    with open(output_path, 'w', encoding='utf-8') as f:
        for chunk in chunks:
            f.write(json.dumps(chunk, ensure_ascii=False) + '\n')
    
    return len(chunks)


def main():
    """Главная функция для запуска чанкинга"""
    
    input_path = DATA_PROCESSED_DIR / "documents.jsonl"
    output_path = DATA_PROCESSED_DIR / "chunks.jsonl"
    
    if not input_path.exists():
        print(f"❌ Ошибка: файл {input_path} не найден")
        print("   Сначала запусти: uv run python scripts/ingest.py")
        return
    
    print(f"📄 Нарезка документов из {input_path}")
    print(f"   Размер чанка: {CHUNK_SIZE}, перекрытие: {CHUNK_OVERLAP}")
    
    num_chunks = chunk_documents(input_path, output_path)
    
    print(f"✅ Создано {num_chunks} чанков")
    print(f"   Файл сохранен: {output_path}")
    
    # Показываем пример чанка
    print("\n📋 Пример первого чанка:")
    with open(output_path, 'r', encoding='utf-8') as f:
        first_chunk = json.loads(f.readline())
        print(f"   doc_id: {first_chunk['doc_id']}")
        print(f"   текст: {first_chunk['text'][:150]}...")


if __name__ == "__main__":
    main()