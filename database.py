"""SQLite database setup and safe, read-only query execution."""
from pathlib import Path
import sqlite3

ROOT = Path(__file__).resolve().parent
DB_PATH = ROOT / "database" / "student.db"
SCHEMA_PATH = ROOT / "database" / "schema.sql"
SEED_PATH = ROOT / "database" / "seed.sql"


def initialize_database(reset: bool = False) -> Path:
    """Create schema and insert deterministic sample data."""
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    if reset and DB_PATH.exists():
        DB_PATH.unlink()

    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("PRAGMA foreign_keys = ON")
        conn.executescript(SCHEMA_PATH.read_text(encoding="utf-8"))
        conn.executescript(SEED_PATH.read_text(encoding="utf-8"))
        conn.commit()
    return DB_PATH


def get_schema_description() -> str:
    """Return table/column/key information for the LLM prompt."""
    with sqlite3.connect(DB_PATH) as conn:
        rows = conn.execute("""
            SELECT m.name, p.name, p.type, p.pk, p."notnull"
            FROM sqlite_master AS m
            JOIN pragma_table_info(m.name) AS p
            WHERE m.type = 'table' AND m.name NOT LIKE 'sqlite_%'
            ORDER BY m.name, p.cid
        """).fetchall()

        foreign_keys = []
        for table in ("Students", "Enrollments", "Marks"):
            for fk in conn.execute(f"PRAGMA foreign_key_list({table})"):
                foreign_keys.append(
                    f"{table}.{fk[3]} -> {fk[2]}.{fk[4]}"
                )

    grouped = {}
    for table, column, data_type, is_pk, not_null in rows:
        grouped.setdefault(table, []).append(
            f"{column} {data_type or 'TEXT'}"
            + (" PRIMARY KEY" if is_pk else "")
            + (" NOT NULL" if not_null and not is_pk else "")
        )

    lines = ["DATABASE TABLES:"]
    for table, columns in grouped.items():
        lines.append(f"- {table}: " + ", ".join(columns))
    lines.append("FOREIGN KEY RELATIONSHIPS:")
    lines.extend(f"- {item}" for item in foreign_keys)
    lines.append(
        "- StudentPerformance is a VIEW joining students, departments, "
        "enrollments, courses and marks."
    )
    return "\n".join(lines)


def _authorizer(action, arg1, arg2, db_name, trigger_name):
    """SQLite-level allowlist: block writes and schema/connection changes."""
    allowed = {
        sqlite3.SQLITE_SELECT,
        sqlite3.SQLITE_READ,
        sqlite3.SQLITE_FUNCTION,
        sqlite3.SQLITE_RECURSIVE,
    }
    if action in allowed:
        return sqlite3.SQLITE_OK
    return sqlite3.SQLITE_DENY


def execute_read_only(sql: str):
    """Execute a single read-only SELECT/WITH statement."""
    if not DB_PATH.exists():
        raise RuntimeError("Database is missing. Run setup first.")

    # URI mode=ro prevents writes even if an application-level check fails.
    uri = f"file:{DB_PATH.as_posix()}?mode=ro"
    conn = sqlite3.connect(uri, uri=True, timeout=5)
    conn.row_factory = sqlite3.Row
    conn.set_authorizer(_authorizer)
    try:
        cursor = conn.execute(sql)  # execute() accepts one statement only.
        rows = [dict(row) for row in cursor.fetchall()]
        columns = [description[0] for description in cursor.description or []]
        return columns, rows
    finally:
        conn.close()
