# Notes — RAG

## Gotchas
- Chunk size is a tradeoff: too big → irrelevant noise; too small → lost context
- Embedding model choice matters more than vector DB choice for retrieval quality
- Always store source + chunk index in metadata, or you can't cite or debug
- "Retrieved" ≠ "relevant" — similarity search returns nearest neighbors, not necessarily useful ones

## Open questions
- How do I evaluate retrieval quality without labeled data?
- When does RAG beat fine-tuning for my use case?
- How do permission-aware retrievals work in multi-tenant systems?

## From OWASP LLM09
> "Poisoning makes the system wrong, inversion makes it leak, jamming makes it silent, and access-control failure makes it indiscriminate."

That one line is basically the RAG security syllabus.