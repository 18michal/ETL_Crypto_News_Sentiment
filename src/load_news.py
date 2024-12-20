from src.db_utils_helper import get_connection


def load_data_to_db(data: list[dict[str, str]]) -> None:
    """Load data from a list of dictionaries into the database."""

    conn = get_connection()
    cursor = conn.cursor()

    insert_query = """
    INSERT INTO dbo.Yahoo_News (Date, Title, Link, Content, PreprocessedContent, Sentiment)
    VALUES (?, ?, ?, ?, ?, ?)
    """

    for row in data:
        cursor.execute(
            insert_query,
            row.get("date"),
            row.get("title"),
            row.get("link"),
            row.get("content"),
            row.get("preprocessed_content"),
            row.get("sentiment"),
        )

    conn.commit()
    conn.close()
