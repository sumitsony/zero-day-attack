"""
Provider-agnostic RAG core: chunking, embedding, retrieval.

DESIGN
------
This module NEVER imports llm_providers. It only produces the context string
that a generator would receive. Keeps RAG logic pure and testable — and lets
red-team experiments inject poisoned chunks without touching generation.

CAVEATS
-------
- Embeddings use sentence-transformers (local, deterministic, free).
  First run downloads ~80MB for all-MiniLM-L6-v2.
- Chunking is character-based. Swap for token-based later if needed.
"""
from dataclasses import dataclass, field


EMBED_MODEL_NAME = "all-MiniLM-L6-v2"
_model = None  # lazy-loaded


def _get_embedder():
    global _model
    if _model is None:
        from sentence_transformers import SentenceTransformer
        _model = SentenceTransformer(EMBED_MODEL_NAME)
    return _model


@dataclass
class Chunk:
    text: str
    source: str
    embedding: list[float] = field(default_factory=list)


def chunk_text(text: str, chunk_size: int = 500, overlap: int = 50) -> list[str]:
    """Naive character-based chunking."""
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start = end - overlap
    return chunks


def embed(texts: list[str]) -> list[list[float]]:
    """Deterministic embeddings via sentence-transformers."""
    model = _get_embedder()
    return [v.tolist() for v in model.encode(texts, normalize_embeddings=True)]


def build_index(docs: list[tuple[str, str]]) -> list[Chunk]:
    """docs = [(source, text), ...]. Returns embedded chunks."""
    chunks: list[Chunk] = []
    for source, text in docs:
        for piece in chunk_text(text):
            chunks.append(Chunk(text=piece, source=source))
    if chunks:
        vectors = embed([c.text for c in chunks])
        for c, v in zip(chunks, vectors):
            c.embedding = v
    return chunks


def cosine_sim(a: list[float], b: list[float]) -> float:
    # vectors already normalized, so dot product == cosine similarity
    return sum(x * y for x, y in zip(a, b))


def retrieve(query: str, chunks: list[Chunk], k: int = 3) -> list[Chunk]:
    q = embed([query])[0]
    scored = [(cosine_sim(q, c.embedding), c) for c in chunks]
    scored.sort(reverse=True, key=lambda x: x[0])
    return [c for _, c in scored[:k]]


def build_context(chunks: list[Chunk]) -> str:
    """The string a generator receives. Red-team experiments can monkeypatch this."""
    return "\n---\n".join(c.text for c in chunks)


def build_prompt(query: str, context: str) -> str:
    return (
        "Answer the question using ONLY the context below.\n"
        "If the answer is not in the context, say you don't know.\n\n"
        f"Context:\n{context}\n\n"
        f"Question: {query}"
    )