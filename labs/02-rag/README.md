# 02 — RAG (Retrieval-Augmented Generation)

## What I'm learning
- How RAG grounds LLM answers in external data without fine-tuning
- The pipeline: chunk → embed → store → retrieve → generate
- Where retrieval quality breaks and how to measure it

## Key ideas
- RAG doesn't train the model; it injects relevant context into the prompt at query time [citation:1][citation:6]
- The retriever is the new attack surface: anything in the corpus can become "trusted context"
- Citations and metadata matter — the LLM needs to know *where* a chunk came from

## Basic pipeline
1. **Source data** — docs, PDFs, Git repos, SQL
2. **Chunking** — split into manageable pieces
3. **Embedding** — convert chunks to vectors
4. **Store** — vector DB with metadata
5. **Retrieve** — similarity search against user query
6. **Generate** — prompt = system + retrieved chunks + user question [citation:1]

## Learning order
1. Build a naive RAG (this folder's `code/`)
2. Break it: what happens with bad chunking? No metadata?
3. Read OWASP LLM09 (Vector & Embedding Weaknesses) [citation:5][citation:13]
4. Study corpus poisoning (DenialRAG, PoisonCraft) [citation:2][citation:3]
5. Add a defense layer and test again

## Links
- Microsoft Learn: RAG concepts [citation:1]
- OWASP Top 10 for LLM Apps 2026 [citation:5]
- DenialRAG (corpus poisoning) [citation:2]
- PoisonCraft (practical poisoning) [citation:3]

## Red-team angle
Corpus poisoning and context injection. See `redteam.md`.