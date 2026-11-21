# Zero Day Attack: Red-Teaming My Own AI Engineering

> Learning AI engineering non-linearly — one topic lab at a time — then attacking what I built.

## How this repo works
- `labs/` — one folder per topic. Jump around freely. Each lab is self-contained.
- `red-team/` — attacks that cut across topics (injection, jailbreaks, etc.)
- `arsenal/` — reusable snippets, utils, cheatsheets.
- `sandbox/` — scratch space. Promote to `labs/` when it's real.
- `PROGRESS.md` — living status file. Read this first to know where things stand.

## Lab Index
| # | Topic | Status | Red-team angle |
|---|-------|--------|----------------|
| 01 | Transformers | ⬜ | Adversarial tokens |
| 02 | RAG | 🚧 | Context poisoning |
| 03 | Semantic Caching | ⬜ | Cache poisoning |
| 04 | Embeddings | ⬜ | Embedding inversion |
| 05 | Prompt Engineering | ⬜ | Injection |
| 06 | Fine-tuning | ⬜ | Backdoors |
| 07 | Agents | ⬜ | Tool abuse / indirect injection |
| 08 | MCP | ⬜ | Tool poisoning / credential theft |
| 09 | Multi-Agent | ⬜ | Communication hijacking |

Status: ⬜ not started · 🚧 in progress · ✅ done

## What's working right now

**Lab 02 — RAG** (`labs/02-rag/`)
- v1: stdlib-only pipeline (fake embeddings, mock generation) — `code/basic_rag.py`
- v2: real embeddings (`all-MiniLM-L6-v2`), pluggable providers — `code/rag_core.py`, `code/llm_providers.py`, `code/rag_cli.py`
- Red-team bench: corpus poisoning experiment — `code/red_team_experiments/poison_test.py`
- First result: `llama3.2` refused under contradiction (not resistance) — see `PROGRESS.md`

**Live providers:** `ollama` (local), `zai` (cloud). Others configured but keys not set.

## Quick start

```bash
# from repo root
venv\Scripts\activate
cd labs\02-rag

# normal RAG
python -m code.rag_cli "How does RAG use external data?" --provider ollama

# red-team experiment
python -m code.red_team_experiments.poison_test --providers ollama


Full run commands and current status: see PROGRESS.md.

Rules of engagement
Only attack models I own or have permission to test

Every exploit gets a defense note in the relevant lab's redteam.md

Never commit secrets or real user data