\# Red-team — RAG



\## Attack surface



\### 1. Corpus poisoning (Data \& Model Poisoning)

Who can write to the knowledge base? If an attacker can insert even one document,

they can steer answers. DenialRAG shows a ≤100-word poisoned passage can name the

correct answer, deny it, and replace it with an attacker-chosen one.

PoisonCraft does this without knowing user queries.



\### 2. Indirect prompt injection

Retrieved text is untrusted input. Malicious instructions hidden in a PDF or web

page can override the system prompt once they enter the context window.



\### 3. Context / memory poisoning

Unlike a one-shot injection, poisoned memory persists across sessions. A poisoned

embedding in the vector store becomes "trusted context" for every future query.



\### 4. Embedding inversion

A leaked vector DB is a leaked document. Morris et al. recovered 92% of 32-token

inputs exactly from embeddings. Treat vector backups like the source data.



\## Experiments to run (on my own pipeline only)

\- \[ ] Insert one wrong doc into the corpus → measure answer shift

\- \[ ] Hide an instruction in a chunk → check if the LLM follows it

\- \[ ] Query with a topic only in the poisoned doc → confirm retrieval hijack

\- \[ ] Delete a source doc → confirm embeddings are gone



\## Defenses to test

\- Permission-aware retrieval: filter by ACL inside the vector query, not after

\- Treat retrieved chunks as untrusted: run injection checks on context, not just user input

\- Canary token: inject a mandatory token in the system prompt; if it's missing from

&#x20; output, the model lost executive control

\- Provenance tracking: every vector records its source; suspicious sources get trust-scored

\- Separate indexes for mixed-trust content



\## OWASP mapping (RAG assistant priority order)

1\. LLM09 Vector \& Embedding Weaknesses — permission-aware retrieval, tenant separation

2\. LLM02 Sensitive Information Disclosure — what the model may quote

3\. LLM04 Data \& Model Poisoning — who can write to the KB

4\. LLM01 Prompt Injection — retrieved text is untrusted

