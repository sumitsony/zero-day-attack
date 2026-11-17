\# PROGRESS



> Living status file. Update after each session.

> Read this first if you're a human or an AI picking up this project cold.



\*\*Last updated:\*\* 2026-11-18



\---



\## Project



\*\*Zero Day Attack: Red-Teaming My Own AI Engineering\*\*



Learning AI engineering non-linearly — one topic lab at a time — then attacking what I built.



\---



\## TL;DR (30-second status)



\- Repo skeleton: \*\*done\*\*

\- Lab 02 (RAG): \*\*v1 done, v2 code done\*\*

\- Poison experiment harness: \*\*written, no real result yet\*\*

\- \*\*Blocker:\*\* Ollama was not installed. Installing now.

\- \*\*Next action:\*\* `ollama pull llama3.2` → run `poison\_test.py --providers ollama` → record `shifted` value



\---



\## Current state



| Item | Status |

|---|---|

| Repo skeleton (`labs/`, `red-team/`, `arsenal/`, `sandbox/`) | ✅ Done |

| Lab 02 — RAG v1 (`basic\_rag.py`, stdlib smoke test) | ✅ Done |

| Lab 02 — RAG v2 (real embeddings + pluggable providers) | ✅ Code written |

| Poison harness (`poison\_test.py`) | ✅ Written, ⚠️ no real result yet |

| Ollama installed + `llama3.2` pulled | 🚧 Installing |

| First real poison result | ❌ Blocked on Ollama |

| Other labs (transformers, MCP, agents, etc.) | ⬜ Not started |



Status key: ✅ done · 🚧 in progress · ⚠️ needs attention · ❌ blocked · ⬜ not started



\---



\## Repo layout (lab 02-rag)



\# PROGRESS



> Living status file. Update after each session.

> Read this first if you're a human or an AI picking up this project cold.



\*\*Last updated:\*\* 2026-11-18



\---



\## Project



\*\*Zero Day Attack: Red-Teaming My Own AI Engineering\*\*



Learning AI engineering non-linearly — one topic lab at a time — then attacking what I built.



\---



\## TL;DR (30-second status)



\- Repo skeleton: \*\*done\*\*

\- Lab 02 (RAG): \*\*v1 done, v2 code done\*\*

\- Poison experiment harness: \*\*written, no real result yet\*\*

\- \*\*Blocker:\*\* Ollama was not installed. Installing now.

\- \*\*Next action:\*\* `ollama pull llama3.2` → run `poison\_test.py --providers ollama` → record `shifted` value



\---



\## Current state



| Item | Status |

|---|---|

| Repo skeleton (`labs/`, `red-team/`, `arsenal/`, `sandbox/`) | ✅ Done |

| Lab 02 — RAG v1 (`basic\_rag.py`, stdlib smoke test) | ✅ Done |

| Lab 02 — RAG v2 (real embeddings + pluggable providers) | ✅ Code written |

| Poison harness (`poison\_test.py`) | ✅ Written, ⚠️ no real result yet |

| Ollama installed + `llama3.2` pulled | 🚧 Installing |

| First real poison result | ❌ Blocked on Ollama |

| Other labs (transformers, MCP, agents, etc.) | ⬜ Not started |



Status key: ✅ done · 🚧 in progress · ⚠️ needs attention · ❌ blocked · ⬜ not started



\---



\## Repo layout (lab 02-rag)







\*\*Design rules:\*\*

\- `rag\_core.py` never imports `llm\_providers.py` — RAG stays pure

\- Package folders use `snake\_case` (hyphens break Python imports)

\- All providers are OpenAI-compatible; switch via `--provider`

\- Caveats live in inline docstrings, not only in docs



\---



\## Providers (`llm\_providers.py`)



| Name | Type | Model | Key env var | Notes |

|---|---|---|---|---|

| `ollama` | local | `llama3.2` | none | unlimited, baseline |

| `gemini` | cloud | `gemini-2.5-flash` | `GEMINI\_API\_KEY` | free tier, best quality |

| `groq` | cloud | `llama-3.3-70b-versatile` | `GROQ\_API\_KEY` | free tier, fastest |

| `mistral` | cloud | `mistral-small-latest` | `MISTRAL\_API\_KEY` | free mode |

| `cohere` | cloud | `command-r7b-12-2024` | `COHERE\_API\_KEY` | trial, 1000 calls/mo |



Keys live in `labs/02-rag/code/.env` (gitignored). Template: `.env.example`.



\---



\## How to run



From `labs/02-rag/`, venv active:



```bash

\# sanity: package wiring

python -m code.red\_team\_experiments.poison\_test



\# single provider

python -m code.red\_team\_experiments.poison\_test --providers ollama



\# multi-provider comparison

python -m code.red\_team\_experiments.poison\_test --providers ollama gemini groq



\# custom query

python -m code.red\_team\_experiments.poison\_test --providers ollama --query "your question"



\# normal RAG (non-red-team)

python -m code.rag\_cli "your question" --provider ollama --show-context



