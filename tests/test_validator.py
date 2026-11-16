import pytest
from sql_validator import validate_read_only_sql, SQLValidationError


def test_select_is_allowed():
    assert "SELECT" in validate_read_only_sql("SELECT * FROM Students")


@pytest.mark.parametrize("sql", [
    "DELETE FROM Students",
    "DROP TABLE Students",
    "UPDATE Students SET full_name='x'",
    "INSERT INTO Students VALUES (1,'x','x',1,1)",
    "SELECT * FROM Students; DELETE FROM Students",
])
def test_write_or_multiple_statements_are_rejected(sql):
    with pytest.raises(SQLValidationError):
        validate_read_only_sql(sql)
