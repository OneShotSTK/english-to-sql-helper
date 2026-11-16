# English-to-SQL Helper

A student-database question answering prototype. Users ask questions in English;
an Ollama language model generates SQLite SQL; the application validates the
statement and executes it against a read-only SQLite connection.

## Features in this starter
- Five related tables: Departments, Students, Courses, Enrollments, Marks
- Foreign keys, CHECK/UNIQUE constraints, indexes and a reporting view
- Ollama-powered few-shot SQL generation
- SQL parsing/allowlist validation with SQLGlot
- SQLite read-only URI and SQLite authorizer as defense in depth
- Streamlit interface, result table, CSV export and session query history
- 40-question evaluation set and starter safety tests

## Requirements
- Python 3.10+
- Ollama installed and running locally
- A model downloaded in Ollama (default: `llama3.1`)

## Setup on macOS
```bash
cd English-to-SQL-Helper
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
ollama pull llama3.1
ollama serve
```
In a second terminal, from the project directory:
```bash
python3 -c "from database import initialize_database; initialize_database(); print('Database ready')"
streamlit run app.py
```
Open the local URL printed by Streamlit.

## Run tests
```bash
pytest -q
```

## Evaluate the 40 questions
```bash
python -m evaluation.evaluate
```
The evaluation runner checks generation and SQL safety. It does not claim
semantic correctness automatically. Compare returned rows with reviewed
expected outputs before reporting accuracy.

## Important safety note
This is an educational prototype, not a production security boundary. It uses
SQLGlot validation, a read-only SQLite URI and a SQLite authorizer. Keep the
database limited to non-sensitive sample data. Review generated SQL and expand
the validator's test suite before deployment.

## Project structure
```text
English-to-SQL-Helper/
├── app.py
├── database.py
├── sql_generator.py
├── sql_validator.py
├── prompts/
│   └── few_shot_examples.py
├── database/
│   ├── schema.sql
│   ├── seed.sql
│   └── student.db       # generated locally
├── evaluation/
│   ├── questions.json
│   └── evaluate.py
├── tests/
│   └── test_validator.py
├── requirements.txt
└── README.md
```
