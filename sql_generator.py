
"""Gemini-based natural-language-to-SQL generation."""

from google import genai
from google.genai import types

from prompts.few_shot_examples import FEW_SHOT_EXAMPLES


class LLMError(RuntimeError):
    pass


def generate_sql(question: str, schema: str, api_key: str) -> str:

    if not api_key:
        raise LLMError("Gemini API key is missing. Please configure it.")

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

DATABASE SCHEMA:
{schema}

EXAMPLES:
{examples}

USER QUESTION:
{question}

SQL:
""".strip()

    try:
        client = genai.Client(api_key=api_key)

        response = client.models.generate_content(
            model="gemini-3.5-flash-lite",
            contents=prompt,
            config=types.GenerateContentConfig(
                temperature=0,
                max_output_tokens=1024,
            ),
        )

        result = (response.text or "").strip()

    except Exception as exc:
        raise LLMError(
            f"Gemini API request failed: {exc}"
        ) from exc

    if result.startswith("```"):
        result = result.replace("```sql", "")
        result = result.replace("```SQL", "")
        result = result.replace("```", "").strip()

    if not result:
        raise LLMError("Gemini returned an empty response.")

    return result
