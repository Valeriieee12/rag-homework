"""Конфигурация проекта"""

import os
from pathlib import Path

# Пути
BASE_DIR = Path(__file__).parent.parent
DATA_RAW_DIR = BASE_DIR / "data" / "raw"
DATA_PROCESSED_DIR = BASE_DIR / "data" / "processed"
DATA_INDEX_DIR = BASE_DIR / "data" / "index"

# Настройки чанкинга
CHUNK_SIZE = 512
CHUNK_OVERLAP = 128

# Настройки поиска
TOP_K = 5
SIMILARITY_THRESHOLD = 0.3

# Создание папок
os.makedirs(DATA_RAW_DIR, exist_ok=True)
os.makedirs(DATA_PROCESSED_DIR, exist_ok=True)
os.makedirs(DATA_INDEX_DIR, exist_ok=True)