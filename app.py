
import time
import pandas as pd
import streamlit as st

from database import (
    initialize_database,
    get_schema_description,
    execute_read_only
)

from sql_generator import generate_sql, LLMError
from sql_validator import validate_read_only_sql, SQLValidationError


# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="English-to-SQL Helper",
    page_icon="🧠",
    layout="wide",
)


# --------------------------------------------------
# APPLICATION HEADER
# --------------------------------------------------

st.title("🧠 English-to-SQL Helper")

st.caption(
    "Ask questions about student data in plain English. "
    "Get safe, explainable SQL."
)


# --------------------------------------------------
# SIDEBAR CONFIGURATION
# --------------------------------------------------

with st.sidebar:

    st.header("⚙️ Configuration")

    st.success("AI Provider: Google Gemini")

    # Read API key securely from Streamlit secrets
    try:
        gemini_api_key = st.secrets["GEMINI_API_KEY"]
    except Exception:
        gemini_api_key = None

    if gemini_api_key:
        st.caption("Gemini API key configured.")
    else:
        st.error("Gemini API key not found.")

    st.divider()

    if st.button(
        "Initialize / repair database",
        use_container_width=True
    ):
        initialize_database()
        st.success("Database is ready.")

    st.caption(
        "The application uses a read-only SQLite connection "
        "for generated queries."
    )


# --------------------------------------------------
# DATABASE INITIALIZATION
# --------------------------------------------------

try:
    initialize_database()
    schema = get_schema_description()

except Exception as exc:
    st.error(f"Database setup failed: {exc}")
    st.stop()


# --------------------------------------------------
# QUERY HISTORY
# --------------------------------------------------

if "history" not in st.session_state:
    st.session_state.history = []


# --------------------------------------------------
# EXAMPLE QUESTIONS
# --------------------------------------------------

examples = [
    "Show all students with their department names.",
    "Find students who scored above 80 in Database Management Systems.",
    "Show the average marks for each course.",
    "Which departments have an average mark above 80?",
    "List the top 5 students by marks in Data Structures.",
]


# --------------------------------------------------
# USER INPUT
# --------------------------------------------------

st.subheader("Ask your database")

question = st.text_area(
    "Write your question in English",
    placeholder="Example: Find students who scored above 80 in DBMS",
    height=100,
)


# --------------------------------------------------
# EXAMPLE QUESTION SELECTION
# --------------------------------------------------

with st.expander("Try an example"):

    for index, example in enumerate(examples):

        if st.button(example, key=f"example_{index}"):

            st.session_state.selected_example = example
            st.rerun()


if "selected_example" in st.session_state:

    question = st.session_state.pop("selected_example")


# --------------------------------------------------
# GENERATE AND EXECUTE SQL
# --------------------------------------------------

generate_clicked = st.button(
    "✨ Generate and run SQL",
    type="primary"
)


if generate_clicked:

    if not question.strip():

        st.warning("Please enter a question first.")

    elif not gemini_api_key:

        st.error(
            "Gemini API key is missing. "
            "Please configure GEMINI_API_KEY in Streamlit secrets."
        )

    else:

        with st.spinner(
            "Asking Google Gemini to generate SQL..."
        ):

            try:

                # Generate SQL using Gemini
                raw_sql = generate_sql(
                    question,
                    schema,
                    api_key=gemini_api_key
                )


                # Check whether clarification is required
                if raw_sql.startswith("NEED_CLARIFICATION:"):

                    st.warning(raw_sql)
                    st.stop()


                # Validate generated SQL
                safe_sql = validate_read_only_sql(raw_sql)


                # Execute query using read-only database connection
                start = time.perf_counter()

                columns, rows = execute_read_only(safe_sql)

                elapsed_ms = (
                    time.perf_counter() - start
                ) * 1000


                # Store query history
                st.session_state.history.insert(0, {

                    "question": question,
                    "sql": safe_sql,
                    "rows": len(rows),
                    "time_ms": elapsed_ms,

                })


                # Display generated SQL
                st.subheader("Generated SQL")

                st.code(
                    safe_sql,
                    language="sql"
                )


                # Display query metrics
                metric1, metric2 = st.columns(2)

                metric1.metric(
                    "Rows returned",
                    len(rows)
                )

                metric2.metric(
                    "Execution time",
                    f"{elapsed_ms:.2f} ms"
                )


                # Display query results
                st.subheader("Query results")

                if rows:

                    dataframe = pd.DataFrame(
                        rows,
                        columns=columns
                    )

                    st.dataframe(
                        dataframe,
                        use_container_width=True
                    )


                    # Download results as CSV
                    csv = dataframe.to_csv(
                        index=False
                    ).encode("utf-8")

                    st.download_button(
                        "⬇️ Download CSV",
                        data=csv,
                        file_name="query_results.csv",
                        mime="text/csv",
                    )

                else:

                    st.info(
                        "The query ran successfully "
                        "but returned no rows."
                    )


            except (LLMError, SQLValidationError) as exc:

                st.error(str(exc))


            except Exception as exc:

                st.error(
                    f"Query execution failed: {exc}"
                )


# --------------------------------------------------
# RECENT QUERY HISTORY
# --------------------------------------------------

st.divider()

st.subheader("🕘 Recent query history")

if st.session_state.history:

    st.dataframe(
        pd.DataFrame(st.session_state.history),
        use_container_width=True,
        hide_index=True,
    )

else:

    st.caption(
        "Your generated queries will appear here."
    )


# --------------------------------------------------
# DATABASE SCHEMA
# --------------------------------------------------

with st.expander("Database schema"):

    st.code(
        schema,
        language="text"
    )
