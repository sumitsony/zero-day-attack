"""
CLI: glue rag_core + llm_providers.

Run from labs/02-rag/:
    python -m code.rag_cli "your question" --provider ollama
    python -m code.rag_cli "your question" --provider gemini --show-context
"""
import argparse
from code.rag_core import build_index, retrieve, build_context, build_prompt
from code import llm_providers


SAMPLE_DOCS = [
    ("doc0", "RAG lets LLMs use external data without fine-tuning."),
    ("doc1", "Chunking splits documents into smaller pieces for embedding."),
    ("doc2", "Retrieval finds the most similar chunks to a user query."),
    ("doc3", "The generator produces an answer using retrieved context."),
]


def main():
    p = argparse.ArgumentParser()
    p.add_argument("query")
    p.add_argument("--provider", default="ollama", choices=list(llm_providers.PROVIDERS))
    p.add_argument("--k", type=int, default=3)
    p.add_argument("--model", default=None)
    p.add_argument("--show-context", action="store_true")
    args = p.parse_args()

    chunks = build_index(SAMPLE_DOCS)
    top = retrieve(args.query, chunks, k=args.k)
    context = build_context(top)
    prompt = build_prompt(args.query, context)

    if args.show_context:
        print("=== RETRIEVED ===")
        print(context)
        print("=== PROMPT SENT ===")
        print(prompt)
        print("=== ANSWER ===")

    print(llm_providers.generate(args.provider, prompt, model=args.model))


if __name__ == "__main__":
    main()