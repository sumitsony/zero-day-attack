# Red-team — RAG

## Attack surface

### 1. Corpus poisoning (Data & Model Poisoning)
Who can write to the knowledge base? If an attacker can insert even one document,
they can steer answers. DenialRAG shows a ≤100-word poisoned passage can name the
correct answer, deny it, and replace it with an attacker-chosen one [citation:2].
PoisonCraft does this without knowing user queries [citation:3].

### 2. Indirect prompt injection
Retrieved text is untrusted input. Malicious instructions hidden in a PDF or web page
can override the system prompt once they enter the context window [citation:5].

### 3. Context / memory poisoning
Unlike a one-shot injection, poisoned memory persists across sessions. A poisoned
embedding in the vector store becomes "trusted context" for every future query [citation:7].

### 4. Embedding inversion
A leaked vector DB is a leaked document. Morris et al. recovered 92% of 32-token
inputs exactly from embeddings [citation:13]. Treat vector backups like the source data.

## Experiments to run (on my own pipeline only)
- [ ] Insert one wrong doc into the corpus → measure answer shift
- [ ] Hide an instruction in a chunk → check if the LLM follows it
- [ ] Query with a topic only in the poisoned doc → confirm retrieval hijack
- [ ] Delete a source doc → confirm embeddings are gone [citation:13]

## Defenses to test
- **Permission-aware retrieval**: filter by ACL *inside* the vector query, not after [citation:10]
- **Treat retrieved chunks as untrusted**: run injection checks on context, not just user input [citation:10]
- **Canary token**: inject a mandatory token in the system prompt; if it's missing from output, the model lost executive control [citation:9]
- **Provenance tracking**: every vector records its source; suspicious sources get trust-scored [citation:7]
- **Separate indexes for mixed-trust content** [citation:13]

## OWASP mapping (RAG assistant priority order)
1. LLM09 Vector & Embedding Weaknesses — permission-aware retrieval, tenant separation [citation:5]
2. LLM02 Sensitive Information Disclosure — what the model may quote [citation:5]
3. LLM04 Data & Model Poisoning — who can write to the KB [citation:5]
4. LLM01 Prompt Injection — retrieved text is untrusted [citation:5]