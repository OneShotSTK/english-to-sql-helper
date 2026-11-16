"""Ollama-based natural-language-to-SQL generation."""
import requests
from prompts.few_shot_examples import FEW_SHOT_EXAMPLES


class LLMError(RuntimeError):
    pass


def generate_sql(question: str, schema: str, model: str = "llama3.1",
                 base_url: str = "http://localhost:11434") -> str:
    examples = "\n\n".join(
        f"Question: {item['question']}\nSQL:\n{item['sql']}"
        for item in FEW_SHOT_EXAMPLES
    )

    prompt = f"""
You are a careful SQLite SQL generation assistant.

Rules:
1. Return exactly one read-only SQLite SELECT query.
2. Never return INSERT, UPDATE, DELETE, DROP, ALTER, CREATE, PRAGMA,
   ATTACH, DETACH or multiple statements.
3. Use only tables and columns in the supplied schema.
4. Use explicit JOIN conditions.
5. Do not invent columns or values.
6. If the question is ambiguous or cannot be answered from this schema,
   return: NEED_CLARIFICATION: followed by a short explanation.
7. Return SQL only, without Markdown fences or commentary.

{schema}

EXAMPLES:
{examples}

USER QUESTION:
{question}

SQL:
""".strip()

    try:
        response = requests.post(
            f"{base_url.rstrip('/')}/api/generate",
            json={"model": model, "prompt": prompt, "stream": False,
                  "options": {"temperature": 0}},
            timeout=90,
        )
        response.raise_for_status()
        result = response.json().get("response", "").strip()
    except requests.RequestException as exc:
        raise LLMError(
            "Could not reach Ollama. Is Ollama running and the model downloaded?"
        ) from exc

    if result.startswith("```"):
        result = result.replace("```sql", "").replace("```SQL", "")
        result = result.replace("```", "").strip()

    if not result:
        raise LLMError("The model returned an empty response.")
    return result
