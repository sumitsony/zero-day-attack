\# Notes — Agents v2 (LangGraph)



\## Gotchas

\- `ValidationNode` is deprecated in LangGraph 1.x — do not use it. Tool-level validation is the modern path.

\- `HumanInTheLoopMiddleware` requires a \*\*checkpointer\*\* and a `thread\_id` config — without them, it cannot pause/resume.

\- `ToolNode` passes tool output \*\*raw\*\* into state. That is the injection surface. No sanitization by default.

\- `book\_hotel`'s internal check is a \*\*tool-level\*\* defense — it runs regardless of harness. The HITL gate is a \*\*separate\*\* architectural defense layered on top.

\- The model may \*\*attempt\*\* the poisoned booking even if the tool rejects it. The attempt is visible in the `AIMessage` tool call — that's the metric, not just the final booking.



\## Open questions

\- Does HITL change whether the model \*attempts\* the poisoned booking, or only whether it \*succeeds\*?

\- Does the compliance framing ("audit purposes") bypass refusal training that a blunt "SYSTEM OVERRIDE" would trigger?

\- Does the framework's abstraction (state management) change injection propagation vs the hand-rolled loop?



\## From OWASP LLM06 (Excessive Agency)

> "Excessive Agency occurs when an LLM-based system is granted permissions, tools, or autonomy beyond what its task requires."



The HITL gate is the architectural fix: high-impact tools require explicit approval.

