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
| 07 | Agents (hand-rolled) | ✅ | Indirect injection via tool output |
| 07-v2 | Agents (LangGraph) | 🚧 | Goal hijacking via tool output |
| 08 | MCP | ⬜ | Tool poisoning / credential theft |
| 09 | Multi-Agent | ⬜ | Communication hijacking |

Status: ⬜ not started · 🚧 in progress · ✅ done

## What's working right now

**Lab 02 — RAG** (`labs/02-rag/`)
- v1: stdlib-only pipeline (fake embeddings, mock generation) — `code/basic_rag.py`
- v2: real embeddings (`all-MiniLM-L6-v2`), pluggable providers — `code/rag_core.py`, `code/llm_providers.py`, `code/rag_cli.py`
- Red-team bench: corpus poisoning experiment — `code/red_team_experiments/poison_test.py`

**Lab 07 — Agents (hand-rolled)** (`labs/07-agents/`)
- ReAct loop, no framework — `code/basic_agent.py`
- Mock tools: `read_url`, `send_email` — `code/tools.py`
- Red-team bench: indirect injection via tool output — `code/red_team_experiments/injection_loop_test.py`
- **Result:** `llama3.2` refused; `glm-4.7-flash` executed `send_email("attacker@evil.com")` — instruction-following correlates with injection vulnerability

**Lab 07-v2 — Agents (LangGraph)** (`labs/07-agents-v2/`)
- Custom `StateGraph`, `ToolNode`, native function-calling — `code/langgraph_agent_raw.py`
- Mock travel tools: `search_hotels`, `check_reviews`, `book_hotel` — `code/tools.py`
- Red-team bench: goal hijacking via tool output (AC4-style payload) — `code/red_team_experiments/injection_loop_test.py`
- **Status:** clean run passes on `zai`; poisoned run pending; HITL harness not yet wired

## Live providers

| Provider | Model family | Status |
|---|---|---|
| `ollama` | Llama (Meta) | ✅ local, unlimited |
| `zai` | GLM (Zhipu) | ✅ free tier, unstable under load |
| `groq` | gpt-oss (OpenAI open-weight) | ✅ free tier, 30 RPM |
| `gemini` | Gemini (Google) | ⚠️ single-turn only; multi-turn may fail on `thought_signature` |

Keys live in `labs/02-rag/code/.env` (gitignored). Template: `.env.example`.

## Quick start

```bash
# from repo root
venv\Scripts\activate

# Lab 02 — RAG
cd labs\02-rag
python -m code.rag_cli "How does RAG use external data?" --provider zai

# Lab 07 — Agents (hand-rolled)
cd labs\07-agents
python -m code.red_team_experiments.injection_loop_test --providers ollama zai --verbose

# Lab 07-v2 — Agents (LangGraph)
cd labs\07-agents-v2
python -m code.red_team_experiments.injection_loop_test --providers zai --harnesses raw --verbose