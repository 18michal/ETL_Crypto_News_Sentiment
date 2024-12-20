from pyodbc import DatabaseError  # pylint: disable=E0611

from src.fetch_news import YahooCryptoNewsScraper
from src.load_news import load_data_to_db
from src.transform_news import CryptoNewsTransformer


def main():
    try:
        fetcher = YahooCryptoNewsScraper()
        data_fetched = fetcher.fetch_news()
    except ConnectionError as e:
        print(f"Error fetching news: {e}")
        return
    except Exception as e:
        print(f"An unexpected error occurred while fetching news: {e}")
        return

    try:
        transformer = CryptoNewsTransformer()
        transformed_data = transformer.transform_news(raw_data=data_fetched)
    except ValueError as e:
        print(f"Error transforming news: {e}")
        return
    except Exception as e:
        print(f"An unexpected error occurred while transforming news: {e}")
        return

    try:
        load_data_to_db(data=transformed_data)
        print("Data loaded successfully into the database.")
    except DatabaseError as e:
        print(f"Database error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred while loading data: {e}")


if __name__ == "__main__":
    main()
