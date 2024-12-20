""" Database connection and utility functions. """

import os

from dotenv import load_dotenv
from pyodbc import Connection, connect  # pylint: disable=E0611

load_dotenv()


def get_connection() -> Connection:
    """Establish and return a database connection."""
    server = os.getenv("DB_SERVER")
    database = os.getenv("DB_NAME")
    username = os.getenv("DB_USER")
    password = os.getenv("DB_PASSWORD")

    conn = connect(
        f"DRIVER={{ODBC Driver 18 for SQL Server}};"
        f"SERVER={server};DATABASE={database};UID={username};PWD={password}"
    )
    return conn


def create_table():
    """Checks if database has table and creates if not."""
    conn = get_connection()
    cursor = conn.cursor()

    check_table_query = """
    IF NOT EXISTS (
        SELECT * 
        FROM INFORMATION_SCHEMA.TABLES 
        WHERE TABLE_SCHEMA = 'dbo' 
        AND TABLE_NAME = 'Yahoo_News'
    )
    BEGIN
        CREATE TABLE dbo.Yahoo_News (
            Date DATETIME NOT NULL,
            Title NVARCHAR(255) NOT NULL,
            Link NVARCHAR(MAX),
            Content NVARCHAR(MAX),
            PreprocessedContent NVARCHAR(MAX),
            Sentiment NVARCHAR(50),
            PRIMARY KEY (Date, Title)
        );
    END;
    """
    cursor.execute(check_table_query)
    conn.commit()
    conn.close()


if __name__ == "__main__":
    create_table()
