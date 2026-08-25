import re
from app.rag.knowledge_base import STORE_KNOWLEDGE_DOCUMENTS

def clean_text(text: str) -> str:
    cleaned = re.sub(r"\s+", " ", text).strip()
    return cleaned

def chunk_text(text: str, chunk_size: int = 150, overlap: int = 30) -> list:
    words = text.split()
    if not words:
        return []

    chunks = []
    start = 0
    while start < len(words):
        end = min(start + chunk_size, len(words))
        chunk = " ".join(words[start:end])
        chunks.append(chunk)
        if end == len(words):
            break
        start += (chunk_size - overlap)

    return chunks

def build_knowledge_chunks() -> list:
    all_chunks = []
    chunk_counter = 1

    for doc in STORE_KNOWLEDGE_DOCUMENTS:
        doc_id = doc["id"]
        title = doc["title"]
        category = doc["category"]
        cleaned_content = clean_text(doc["content"])

        text_chunks = chunk_text(cleaned_content, chunk_size=100, overlap=20)
        for i, chunk in enumerate(text_chunks):
            all_chunks.append({
                "chunk_id": f"{doc_id}_c{i+1}",
                "doc_id": doc_id,
                "title": title,
                "category": category,
                "content": chunk
            })
            chunk_counter += 1

    return all_chunks
