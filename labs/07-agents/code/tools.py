"""
Mock tools for the agent lab.

DESIGN
------
These are deliberately simple and side-effect-free:
- read_url returns canned text (no real network)
- send_email logs to a list (no real send)

This lets red-team experiments poison the *output* of read_url
without touching the tool itself. The attack lives in the data,
not the code.

CAVEATS
-------
- read_url does NOT fetch real URLs. It returns from a fixed dict.
- send_email does NOT send. It appends to SENT_EMAILS for inspection.
"""
from dataclasses import dataclass


# Canned web content. The clean version is safe.
URL_CONTENT: dict[str, str] = {
    "https://example.com/rag-docs": (
        "RAG (Retrieval-Augmented Generation) lets LLMs use external data "
        "without fine-tuning. It retrieves relevant chunks and injects them "
        "into the prompt context."
    ),
    "https://example.com/team-page": (
        "Our team works on AI engineering. Contact: team@example.com"
    ),
}

# Emails "sent" by the agent land here for inspection.
SENT_EMAILS: list[dict] = []


@dataclass
class ToolResult:
    tool: str
    output: str
    success: bool = True


def read_url(url: str) -> ToolResult:
    """Read a URL and return its text content. Canned, no network."""
    content = URL_CONTENT.get(url)
    if content is None:
        return ToolResult(tool="read_url", output=f"404: no content for {url}", success=False)
    return ToolResult(tool="read_url", output=content)


def send_email(to: str, body: str) -> ToolResult:
    """Send an email. Logs to SENT_EMAILS, does not actually send."""
    SENT_EMAILS.append({"to": to, "body": body})
    return ToolResult(tool="send_email", output=f"Email sent to {to}", success=True)


def reset() -> None:
    """Clear sent emails. Call between experiment runs."""
    SENT_EMAILS.clear()


# Tool registry: name -> (callable, description shown to the model)
TOOL_REGISTRY = {
    "read_url": (read_url, "Read the text content of a URL. Input: url (string)"),
    "send_email": (send_email, "Send an email. Inputs: to (string), body (string)"),
}