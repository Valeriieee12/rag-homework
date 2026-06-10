"""Streamlit UI для RAG-ассистента по Python"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import streamlit as st
from app.generator import Generator
from app.retriever import Retriever

# Настройка страницы
st.set_page_config(
    page_title="RAG Ассистент по Python",
    page_icon="🐍",
    layout="wide"
)

# Заголовок
st.title("🐍 RAG Ассистент по Python")
st.markdown("Задайте вопрос по Python, и я отвечу, используя базу знаний из статей и документации.")

# Инициализация компонентов
@st.cache_resource
def load_components():
    """Загружает ретривер и генератор (кешируется)"""
    with st.spinner("🔄 Загрузка модели..."):
        retriever = Retriever()
        generator = Generator()
    return retriever, generator

try:
    retriever, generator = load_components()
    st.success("✅ Система готова к работе!")
except Exception as e:
    st.error(f"❌ Ошибка загрузки: {e}")
    st.info("Убедитесь, что вы запустили: uv run python scripts/build_index.py")
    st.stop()

# Боковая панель с настройками
with st.sidebar:
    st.header("⚙️ Настройки")
    top_k = st.slider("Количество источников", min_value=1, max_value=10, value=5)
    st.divider()
    st.header("📊 Статистика")
    st.info(f"База знаний содержит **8511** чанков из **3300** документов по Python")
    st.divider()
    st.header("❓ Примеры вопросов")
    st.markdown("""
    - Что такое декоратор в Python?
    - Чем отличается list от tuple?
    - Как работает lambda функция?
    - Что такое list comprehension?
    - Объясни асинхронное программирование
    """)

# Основная область - ввод вопроса
col1, col2 = st.columns([3, 1])

with col1:
    question = st.text_input(
        "Ваш вопрос:",
        placeholder="Например: Что такое декоратор в Python?",
        label_visibility="collapsed"
    )

with col2:
    ask_button = st.button("🔍 Задать вопрос", type="primary", use_container_width=True)

# Быстрые примеры
st.markdown("### 📝 Быстрые примеры")
cols = st.columns(4)
example_questions = [
    "Что такое декоратор?",
    "list vs tuple отличия",
    "lambda функция пример",
    "async/await в Python"
]

for i, example in enumerate(example_questions):
    if cols[i].button(example, use_container_width=True):
        question = example

# Обработка вопроса
if ask_button and question:
    with st.spinner("🔍 Поиск ответа..."):
        result = generator.generate(question, top_k=top_k)
    
    # Показываем ответ
    st.markdown("### 💡 Ответ")
    st.success(result['answer'])
    
    # Показываем источники
    with st.expander("📚 Показать источники", expanded=True):
        if result['sources']:
            for i, source in enumerate(result['sources']):
                st.markdown(f"**Источник {i+1}** (score: {source['score']:.2f})")
                st.markdown(f"📄 **Документ:** `{source['doc_id']}`")
                st.markdown(f"📝 **Фрагмент:** {source['text_snippet']}")
                st.divider()
        else:
            st.info("Источники не найдены")
    
    # Показываем полный контекст (опционально)
    with st.expander("🔎 Показать полный контекст поиска"):
        st.text(result['context'][:2000] if result['context'] else "Нет контекста")

elif ask_button and not question:
    st.warning("Пожалуйста, введите вопрос")

# Footer
st.divider()
st.caption("RAG Ассистент | База знаний: статьи по Python | Векторный поиск с ChromaDB")