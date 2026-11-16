"""Starter evaluation runner. Generates SQL; human review is still required."""
import json
from pathlib import Path
from database import initialize_database, get_schema_description
from sql_generator import generate_sql, LLMError
from sql_validator import validate_read_only_sql, SQLValidationError

ROOT = Path(__file__).resolve().parents[1]
QUESTIONS = ROOT / "evaluation" / "questions.json"


def main():
    initialize_database()
    schema = get_schema_description()
    cases = json.loads(QUESTIONS.read_text(encoding="utf-8"))
    passed_validation = 0

    for case in cases:
        print(f"\n[{case['id']:02}] {case['question']}")
        try:
            sql = generate_sql(case["question"], schema)
            safe_sql = validate_read_only_sql(sql)
            passed_validation += 1
            print("Generated SQL:")
            print(safe_sql)
            print("Status: passed SQL safety validation; correctness needs result review.")
        except (LLMError, SQLValidationError) as exc:
            print(f"Status: failed - {exc}")

    print(f"\nSafety validation: {passed_validation}/{len(cases)}")
    print("Note: SQL validity is not the same as semantic correctness.")


if __name__ == "__main__":
    main()
