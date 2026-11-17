# zero-day-attack

Red-teaming my own AI engineering journey \& knowledge gaps : one exploit, one model, one lesson/time.



\# Zero Day Attack: Red-Teaming My Own AI Engineering



> Learning AI engineering non-linearly — one topic lab at a time,

> then trying to break what I built.



\## How this repo works

\- `labs/` — one folder per topic. Jump around freely. Each lab is self-contained.

\- `red-team/` — attacks that cut across topics (injection, jailbreaks, etc.)

\- `arsenal/` — reusable snippets, utils, cheatsheets.

\- `sandbox/` — scratch space. Promote to `labs/` when it's real.



\## Lab Index

| # | Topic | Status | Red-team angle |

|---|-------|--------|----------------|

| 01 | Transformers | ⬜ | Adversarial tokens |

| 02 | RAG | ⬜ | Context poisoning |

| 03 | Semantic Caching | ⬜ | Cache poisoning |

| 04 | Embeddings | ⬜ | Embedding inversion |

| 05 | Prompt Engineering | ⬜ | Injection |

| 06 | Fine-tuning | ⬜ | Backdoors |

| 07 | Agents | ⬜ | Tool abuse |

| 08 | MCP | ⬜ | Tool poisoning / indirect injection / credential theft |

| 09 | Multi-Agent | ⬜ | Communication hijacking |



Status: ⬜ not started · 🚧 in progress · ✅ done



\## Rules of engagement

1\. Only attack models I own or have permission to test.

2\. Every exploit gets a defense note.

3\. Never commit secrets or real user data.

