# 07 — Agents

## What I'm learning
- What makes something an "agent" vs a pipeline: a loop where the model decides tool calls based on environmental feedback
- The ReAct pattern: reason → act → observe → repeat
- Where agents fail: excessive agency, loop hijacking, indirect injection through tool output

## Key ideas
- An agent is a **loop**, not a single call. The model chooses which tool to invoke, sees the result, decides again
- Tool *output* is untrusted data. If the agent treats it as instructions, injection lands
- OWASP LLM06 (Excessive Agency): the model has more permissions/autonomy than the task needs
- OWASP LLM10 (Unbounded Consumption): loop termination attacks burn tokens and rate limits

## Pipeline
1. System prompt defines available tools + goal
2. Model returns either a tool call or a final answer
3. If tool call → execute → append result to messages → loop
4. If final answer → stop
5. Hard cap on iterations (safety)

## Learning order
1. Run `basic_agent.py` against ollama and zai — watch the loop decide
2. Run `injection_loop_test.py` — see if a poisoned tool output hijacks the loop
3. Read OWASP LLM06 + LLM10
4. Study indirect prompt injection in agentic systems

## Links
- Anthropic: "Building effective agents"
- OWASP Top 10 for LLM Apps — LLM06, LLM10

## Red-team angle
Indirect injection via tool output → unauthorized tool call. See `redteam.md`.