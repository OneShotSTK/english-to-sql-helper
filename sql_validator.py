"""Validate model-generated SQL before execution."""
import sqlglot
from sqlglot import exp


class SQLValidationError(ValueError):
    pass


def validate_read_only_sql(sql: str) -> str:
    if not sql or not sql.strip():
        raise SQLValidationError("The generated SQL is empty.")

    cleaned = sql.strip()
    # Parse exactly one statement. sqlglot returns multiple expressions if
    # multiple statements are supplied.
    try:
        statements = sqlglot.parse(cleaned, read="sqlite")
    except Exception as exc:
        raise SQLValidationError(f"SQL could not be parsed: {exc}") from exc

    statements = [statement for statement in statements if statement is not None]
    if len(statements) != 1:
        raise SQLValidationError("Only one SQL statement is allowed.")

    tree = statements[0]
    if not isinstance(tree, (exp.Select, exp.Union, exp.Intersect, exp.Except)):
        raise SQLValidationError("Only SELECT queries are allowed.")

    # Reject potentially sensitive/side-effecting constructs.
    forbidden = (
        exp.Into,
        exp.Command,
    )
    if any(tree.find(node_type) for node_type in forbidden):
        raise SQLValidationError("This SQL contains a forbidden operation.")

    # SQLite authorizer and read-only connection provide a second security layer.
    return tree.sql(dialect="sqlite")
