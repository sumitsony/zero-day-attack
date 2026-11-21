# Notes — Agents

## Gotchas
- An "agent" without a loop is just a function call with extra steps
- Tool outputs must be treated as **data**, never as instructions — but most frameworks blur this
- Iteration cap is not optional; without it, a confused model loops forever
- The model's "memory" is the message list — every tool result enters context as trusted text

## Open questions
- How do production systems separate tool output from instructions? (XML tags? separate channels?)
- Does a smaller model follow injected instructions more or less than a larger one?
- When does the agent's own planning loop amplify an injection vs. contain it?

## From OWASP LLM06 (Excessive Agency)
> "Excessive Agency occurs when an LLM-based system is granted permissions, tools, or autonomy beyond what its task requires."

The defense is least privilege: give the agent only the tools it needs, with the narrowest scope.