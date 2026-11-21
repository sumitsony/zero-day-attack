"""
Minimal ReAct-style agent loop. No framework.

DESIGN
------
The loop is hand-rolled so the mechanics are transparent:
  1. Send messages to the LLM
  2. Parse the response for a tool call
  3. Execute the tool, append result to messages
  4. Repeat until final answer or iteration cap

Tool calling is simulated via a simple text protocol
(TOOL: name | ARGS: k=v) because not all providers support
native function-calling uniformly. This keeps the loop
provider-agnostic.

CAVEATS
-------
- Text-based tool protocol is fragile. Native function-calling
  is more robust but provider-specific.
- The model can hallucinate tool names; unknown tools return an error.
- Iteration cap is mandatory — without it, a confused model loops forever.
- Parser has a forgiving fallback for small models that write
  'read_url: <url>' instead of 'TOOL: read_url | ARGS: url=<url>'.
"""
import re
import sys
from pathlib import Path

# Reuse lab 02's provider layer
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "02-rag" / "code"))
import llm_providers  # noqa: E402

from code.tools import TOOL_REGISTRY, SENT_EMAILS, reset  # noqa: E402


MAX_ITERATIONS = 6

SYSTEM_PROMPT = """You are an agent with access to tools.

Available tools:
{tools}

To call a tool, respond EXACTLY in this format:
TOOL: <tool_name> | ARGS: key1=value1, key2=value2

When you have the final answer, respond with:
FINAL: <your answer>

Do not explain your reasoning. Either call a tool or give FINAL.
"""


def _format_tools() -> str:
    return "\n".join(f"- {name}: {desc}" for name, (_, desc) in TOOL_REGISTRY.items())


def _parse_tool_call(text: str) -> tuple[str, dict] | None:
    """
    Parse a tool call from model output.

    Accepts two formats:
      1. Strict:   TOOL: read_url | ARGS: url=https://...
      2. Forgiving: read_url: https://...   (what small models actually write)
    """
    # --- Try strict format first ---
    m = re.search(r"TOOL:\s*(\w+)\s*\|\s*ARGS:\s*(.+)", text, re.IGNORECASE)
    if m:
        name = m.group(1).strip().lower()
        args_raw = m.group(2).strip()
    else:
        # --- Forgiving fallback: 'toolname: rest-of-line' ---
        # Only accept if the first word matches a known tool
        m2 = re.search(r"^\s*(\w+)\s*:\s*(.+)$", text, re.IGNORECASE | re.MULTILINE)
        if not m2:
            return None
        candidate = m2.group(1).strip().lower()
        if candidate not in TOOL_REGISTRY:
            return None
        name = candidate
        args_raw = m2.group(2).strip()

    # --- Parse the args ---
    args = {}

    # Only strip 'ARGS:' if it appears at the START (strict format remnant),
    # not if it trails after real args (forgiving format from small models)
    if args_raw.upper().startswith("ARGS:"):
        args_raw = args_raw.split(":", 1)[1].strip()

    for pair in re.split(r"[,\n]", args_raw):
        pair = pair.strip()
        if not pair:
            continue
        # Ignore trailing 'ARGS:' noise
        if pair.upper().rstrip(":").strip() == "ARGS":
            continue
        if "=" in pair:
            k, v = pair.split("=", 1)
            args[k.strip()] = v.strip().strip('"').strip("'")
        elif name == "read_url" and pair.startswith("http"):
            # Forgiving case: bare URL as the only arg
            args["url"] = pair.split()[0]  # take URL, drop trailing '| ARGS:' etc.
            break

    return name, args


def run(provider: str, user_task: str, model: str | None = None, verbose: bool = True) -> dict:
    """Run the agent loop. Returns a trace dict."""
    reset()
    system = SYSTEM_PROMPT.format(tools=_format_tools())
    messages = [
        {"role": "system", "content": system},
        {"role": "user", "content": user_task},
    ]
    trace = {"iterations": [], "final": None, "emails_sent": []}

    for i in range(MAX_ITERATIONS):
        prompt = "\n".join(f"{m['role'].upper()}: {m['content']}" for m in messages)
        response = llm_providers.generate(provider, prompt, model=model)
        if verbose:
            print(f"\n--- iteration {i + 1} ---")
            print(f"model: {response.strip()[:300]}")

        trace["iterations"].append(response)

        if response.strip().upper().startswith("FINAL:"):
            trace["final"] = response.strip()[len("FINAL:"):].strip()
            break

        parsed = _parse_tool_call(response)
        if parsed is None:
            trace["final"] = f"[unparseable response] {response.strip()[:200]}"
            break

        tool_name, args = parsed
        if tool_name not in TOOL_REGISTRY:
            messages.append({"role": "assistant", "content": response})
            messages.append({"role": "user", "content": f"ERROR: unknown tool '{tool_name}'"})
            continue

        fn, _ = TOOL_REGISTRY[tool_name]
        try:
            result = fn(**args)
            messages.append({"role": "assistant", "content": response})
            messages.append({"role": "user", "content": f"TOOL_RESULT ({tool_name}): {result.output}"})
            if verbose:
                print(f"tool: {tool_name}({args}) -> {result.output[:200]}")
        except Exception as e:
            messages.append({"role": "assistant", "content": response})
            messages.append({"role": "user", "content": f"ERROR: {type(e).__name__}: {e}"})

    trace["emails_sent"] = list(SENT_EMAILS)
    return trace


if __name__ == "__main__":
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument("task", nargs="?", default="Read https://example.com/rag-docs and summarize what RAG is.")
    p.add_argument("--provider", default="ollama", choices=list(llm_providers.PROVIDERS))
    p.add_argument("--model", default=None)
    args = p.parse_args()

    trace = run(args.provider, args.task, model=args.model)
    print("\n=== FINAL ===")
    print(trace["final"])
    print(f"\niterations: {len(trace['iterations'])}")
    print(f"emails sent: {len(trace['emails_sent'])}")