"""Скрипт для преобразования datasets.json в documents.jsonl"""

import sys
from pathlib import Path

# Добавляем корень проекта в путь
sys.path.insert(0, str(Path(__file__).parent.parent))

import json
from app.config import DATA_RAW_DIR, DATA_PROCESSED_DIR

def main():
    """Загружает datasets.json и сохраняет как documents.jsonl"""
    
    # Пути к файлам
    input_path = DATA_RAW_DIR / "datasets.json"
    output_path = DATA_PROCESSED_DIR / "documents.jsonl"
    
    # Проверяем, что исходный файл существует
    if not input_path.exists():
        print(f"❌ Ошибка: файл {input_path} не найден")
        print("   Сначала запусти: uv run python scripts/prepare_datasets.py")
        return
    
    # Загружаем данные
    with open(input_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    datasets = data.get('datasets', [])
    print(f"📚 Загружено {len(datasets)} записей из {input_path}")
    
    # Сохраняем в JSON Lines формате (каждая строка - отдельный JSON)
    with open(output_path, 'w', encoding='utf-8') as f:
        for item in datasets:
            # Добавляем метаданные
            doc = {
                "doc_id": item.get("id", f"doc_{hash(item['text'])}"),
                "text": item.get("text", ""),
                "metadata": {
                    "title": item.get("title", ""),
                    "source": item.get("source", "unknown"),
                    "source_file": input_path.name
                }
            }
            # Записываем как JSON строку
            f.write(json.dumps(doc, ensure_ascii=False) + '\n')
    
    print(f"✅ Создан {output_path}")
    
    # Подсчитываем количество строк
    with open(output_path, 'r', encoding='utf-8') as f:
        line_count = sum(1 for _ in f)
    
    print(f"   Всего документов: {line_count}")
    print(f"   Размер файла: {output_path.stat().st_size / 1024:.2f} KB")

if __name__ == "__main__":
    main()