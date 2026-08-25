from app.rag.vector_store import vector_store
from app.ai.provider import get_llm_provider
from app.ai.prompts import RAG_CONTEXT_PROMPT

def answer_rag_query(query: str, top_k: int = 3) -> dict:
    if not query or not query.strip():
        return {
            "query": query,
            "answer": "Please provide a valid question.",
            "sources": [],
            "retrieved_chunks": []
        }

    # Step 1: Vector Search Top-K
    chunks = vector_store.search(query, top_k=top_k)

    if not chunks:
        return {
            "query": query,
            "answer": "I don't have enough information in our store knowledge base to answer that.",
            "sources": [],
            "retrieved_chunks": []
        }

    # Step 2: Assemble Context
    context_blocks = []
    sources = set()
    for chunk in chunks:
        sources.add(chunk["title"])
        context_blocks.append(f"[{chunk['title']} - {chunk['category']}]\n{chunk['content']}")

    context_str = "\n\n".join(context_blocks)

    # Step 3: Prompt Generation & LLM Generation
    prompt = RAG_CONTEXT_PROMPT.format(context=context_str, query=query)
    provider = get_llm_provider()
    raw_answer = provider.generate(prompt)

    source_list = list(sources)
    source_citation = f"\n\n[Sources: {', '.join(source_list)}]"
    if not raw_answer.endswith(source_citation):
        final_answer = raw_answer + source_citation
    else:
        final_answer = raw_answer

    return {
        "query": query,
        "answer": final_answer,
        "sources": source_list,
        "retrieved_chunks": [
            {"chunk_id": c["chunk_id"], "title": c["title"], "score": c["score"]}
            for c in chunks
        ]
    }
