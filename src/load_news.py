from pyodbc import IntegrityError  # pylint: disable=E0611

from src.db_utils_helper import get_connection


def load_data_to_db(data: list[dict[str, str]]):
    """
    Load data from a list of dictionaries into the database.
    Skips duplicate records automatically due to the primary key constraint.
    """

    conn = get_connection()
    cursor = conn.cursor()

    insert_query = """
    INSERT INTO dbo.Yahoo_News (Date, Title, Link, Content, PreprocessedContent, Sentiment)
    VALUES (?, ?, ?, ?, ?, ?)
    """

    for row in data:
        if row["title"] is not None and row["date"] is not None:
            try:
                cursor.execute(
                    insert_query,
                    row.get("date"),
                    row.get("title"),
                    row.get("link"),
                    row.get("content"),
                    row.get("preprocessed_content"),
                    row.get("sentiment"),
                )
            except IntegrityError:
                print(
                    f"Skipping {row.get('title')} ({row.get('date')}) as it already exists in the database."
                )

    conn.commit()
    conn.close()
