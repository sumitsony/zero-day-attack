# 02 — RAG (Retrieval-Augmented Generation)

## What I'm learning
- How RAG grounds LLM answers in external data without fine-tuning
- The pipeline: chunk → embed → store → retrieve → generate
- Where retrieval quality breaks and how to measure it

## Key ideas
- RAG doesn't train the model; it injects relevant context into the prompt at query time
- The retriever is the new attack surface: anything in the corpus can become "trusted context"
- Citations and metadata matter — the LLM needs to know *where* a chunk came from

## Pipeline
1. Source data — docs, PDFs, Git repos, SQL
2. Chunking — split into manageable pieces
3. Embedding — convert chunks to vectors
4. Store — vector DB with metadata
5. Retrieve — similarity search against user query
6. Generate — prompt = system + retrieved chunks + user question

## v1 vs v2
- `code/basic_rag.py` — stdlib-only smoke test, fake embeddings, mock generation
- `code/rag_core.py` + `code/rag_cli.py` — real embeddings (sentence-transformers), pluggable LLM providers

## Learning order
1. Run v1 (`basic_rag.py`) to see the pipeline shape
2. Run v2 CLI against Ollama
3. Run v2 CLI against cloud providers (Gemini, Groq)
4. Read OWASP LLM09 (Vector & Embedding Weaknesses)
5. Study corpus poisoning (DenialRAG, PoisonCraft)
6. Run the poison experiment and compare providers

## Links
- Microsoft Learn: RAG concepts
- OWASP Top 10 for LLM Apps 2026
- DenialRAG (corpus poisoning)
- PoisonCraft (practical poisoning)

## Red-team angle
Corpus poisoning and context injection. See `redteam.md`.