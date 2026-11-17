"""
Minimal RAG pipeline for learning.

PURPOSE
-------
Smoke-test the full pipeline (chunk -> embed -> retrieve -> generate)
using ONLY the Python standard library. No pip installs, no API keys.

CAVEATS (read before trusting the output)
-----------------------------------------
1. EMBEDDINGS ARE FAKE.
   embed() uses Python's built-in hash(). That is NOT a semantic embedding.
   - It does not capture meaning, only a crude byte pattern.
   - Retrieval results are therefore NOT meaningful.
   - This is only to prove the *plumbing* works.

2. hash() IS RANDOMIZED PER PROCESS ON WINDOWS.
   Python randomizes string hashing per interpreter run (PYTHONHASHSEED),
   so retrieval order can change between runs. Not reproducible.
   -> Fix in v2: swap embed() for a real model (e.g. sentence-transformers).

3. CHUNKING IS CHARACTER-BASED.
   chunk_text() splits on raw characters, not tokens.
   Real pipelines should chunk on tokens or semantic boundaries.

4. GENERATION IS A MOCK.
   generate() just echoes the retrieved context. No real LLM is called.
   -> Fix in v2: swap generate() for a real LLM call.

WHAT THIS FILE IS FOR
---------------------
- Confirming the data flow is correct before adding real components
- A reference for the interfaces that v2 will implement
"""
from dataclasses import dataclass, field
import math

@dataclass
class Chunk:
    text: str
    source: str
    embedding: list[float] = field(default_factory=list)

def chunk_text(text: str, chunk_size: int = 500, overlap: int = 50) -> list[str]:
    """Naive character-based chunking. Swap for token-based later."""
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start = end - overlap
    return chunks

def embed(text: str) -> list[float]:
    """
    PLACEHOLDER — NOT a real embedding.

    Uses Python's built-in hash() to produce a fixed-length vector.
    Caveats:
      - hash() is NOT semantic (no meaning captured)
      - hash() is randomized per process on Windows (not reproducible)
    Replace with a real embedding call in v2.
    """
    return [float((hash(text + str(i)) % 100) / 100) for i in range(8)]

def cosine_sim(a: list[float], b: list[float]) -> float:
    dot = sum(x * y for x, y in zip(a, b))
    na = math.sqrt(sum(x * x for x in a))
    nb = math.sqrt(sum(y * y for y in b))
    return dot / (na * nb + 1e-9)

def retrieve(query: str, chunks: list[Chunk], k: int = 3) -> list[Chunk]:
    """Top-k by cosine similarity. Order is non-deterministic given fake embeddings."""
    q_emb = embed(query)
    scored = [(cosine_sim(q_emb, c.embedding), c) for c in chunks]
    scored.sort(reverse=True, key=lambda x: x[0])
    return [c for _, c in scored[:k]]

def generate(query: str, context: list[Chunk]) -> str:
    """
    PLACEHOLDER — NOT a real LLM call.
    Echoes retrieved context so you can eyeball what would have been sent to a model.
    Replace with a real LLM call in v2.
    """
    ctx = "\n---\n".join(c.text for c in context)
    return f"[LLM would answer based on:]\n{ctx}\n\nQuestion: {query}"

if __name__ == "__main__":
    docs = [
        "RAG lets LLMs use external data without fine-tuning.",
        "Chunking splits documents into smaller pieces for embedding.",
        "Retrieval finds the most similar chunks to a user query.",
        "The generator produces an answer using retrieved context.",
    ]
    chunks = []
    for i, d in enumerate(docs):
        for j, piece in enumerate(chunk_text(d)):
            chunks.append(Chunk(text=piece, source=f"doc{i}", embedding=embed(piece)))

    query = "How does RAG use external data?"
    results = retrieve(query, chunks, k=2)
    print("Retrieved:", [r.source for r in results])
    print(generate(query, results))