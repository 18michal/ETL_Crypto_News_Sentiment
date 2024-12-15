import logging
from time import sleep
from typing import Optional

import requests
from bs4 import BeautifulSoup, Tag

from project_config import YahooConfig

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class YahooCryptoNewsScraper(YahooConfig):
    """A class to scrape cryptocurrency news articles from Yahoo Finance."""

    def __init__(self) -> None:
        self.site_url = self.URL
        self.unwanted_start = self.ARTICLE_UNWANTED_CONTENT_START
        self.unwanted_end = self.ARTICLE_UNWANTED_CONTENT_END

    def fetch_news(self) -> list[dict[str, Optional[str]]]:
        """
        Main function to fetch and process cryptocurrency news articles.

        This function retrieves a list of cryptocurrency news articles from the given
        `site_url` in the configuration, fetches additional content and publication dates for
        each article, and stores the results in a structured format.

        Returns:
            list[dict[str, Optional[str]]]: A list of dictionaries, where each dictionary
            represents an article with the following keys:
                - "title" (str): The title of the article.
                - "link" (str): The URL of the article.
                - "content" (Optional[str]): The content of the article or `None` if unavailable.
                - "date" (Optional[str]): The date of the article or `None` if unavailable.

        Notes:
            - The function includes a delay of 1 second between processing each article
            to avoid overwhelming the server with requests.
            - Logs are generated to indicate successful fetching and processing.

        Example:
            >>> fetcher = CryptoNewsFetcher()
            >>> fetcher.fetch_news()
            [
                {
                    "title": "Bitcoin Hits All-Time High",
                    "link": "https://finance.yahoo.com/news/bitcoin-hits-high",
                    "content": "Bitcoin reached a new all-time high...",
                    "date": "2024-12-15T10:00:00Z"
                },
                ...
            ]
        """
        crypto_news = self._fetch_crypto_news()

        for article in crypto_news:
            if isinstance(article["link"], str) and isinstance(article["title"], str):

                content = self._fetch_article_content(
                    article_url=article["link"], article_title=article["title"]
                )
                article["content"] = content

                date = self._fetch_article_date(article_url=article["link"])
                article["date"] = date
                sleep(1)

        logger.info("Crypto News fetched and processed successfully.")

        return crypto_news

    def _fetch_crypto_news(self) -> list[dict[str, Optional[str]]]:
        """Fetch titles and links from the main page"""
        try:
            response = requests.get(self.site_url, timeout=10)

            if response.status_code != 200:
                logger.error("Failed to fetch page: %s", response.status_code)
                return []

            soup = BeautifulSoup(response.content, "html.parser")
            sections = soup.find_all("section", {"role": "article"})

            articles = []
            for section in sections:
                link_tag = section.find("a", {"aria-label": True, "href": True})
                title_tag = section.find("h3")

                if link_tag and title_tag:
                    title = title_tag.text.strip()
                    link = link_tag["href"]

                    # Ensure absolute URLs
                    if not link.startswith("http"):
                        link = f"https://finance.yahoo.com{link}"

                    articles.append({"title": title, "link": link})

            return articles
        except requests.RequestException as e:
            logger.exception("An error occurred while fetching the URL: %s", e)
            return []

    def _fetch_article_content(
        self, article_url: str, article_title: str
    ) -> str | None:
        """
        Extracts and cleans the main content of an article from a given URL.

        Parameters:
            article_url (str): The URL of the article.

        Returns:
            str: The cleaned article content, or None if the extraction fails.
        """
        try:
            response = requests.get(article_url, timeout=10)
            response.raise_for_status()

        except requests.RequestException as e:
            logger.error("Failed to fetch page at %s: %s", article_url, e)
            return None

        soup = BeautifulSoup(response.content, "html.parser")

        content_tags = soup.find_all(["p", "h1", "h2", "h3", "h4", "h5", "h6"])
        article_content = "\n".join(
            tag.get_text(strip=True) for tag in content_tags if tag.get_text(strip=True)
        )

        # Remove unwanted sections from the beginning
        for unwanted in self.unwanted_start:
            if article_content.startswith(unwanted):
                article_content = article_content[len(unwanted) :].strip()

        # Remove unwanted sections from the end
        for unwanted in self.unwanted_end:
            if unwanted in article_content:
                article_content = article_content.split(unwanted)[0].strip()

        # Remove the first line (topic)
        possible_article_title = article_content.splitlines()
        if article_title == possible_article_title[0]:
            article_content = "\n".join(possible_article_title[1:]).strip()

        return article_content if article_content else None

    def _fetch_article_date(self, article_url: str) -> str | None:
        """
        Extracts the publication date of an article from a given URL.

        Parameters:
            article_url (str): The URL of the article.

        Returns:
            str: The publication date, or None if the extraction fails.
        """
        try:
            response = requests.get(article_url, timeout=10)
            response.raise_for_status()

        except requests.RequestException as e:
            logger.error("Failed to fetch page at %s: %s", article_url, e)
            return None

        soup = BeautifulSoup(response.content, "html.parser")

        article_date: Optional[str] = None
        time_tag = soup.find("time")
        if isinstance(time_tag, Tag):
            datetime_value = time_tag.get("datetime")
            text_value = time_tag.get_text(strip=True)

            if isinstance(datetime_value, str):
                article_date = datetime_value
            elif isinstance(text_value, str):
                article_date = text_value
            else:
                logger.warning(
                    "Time tag found, but it does not contain a valid datetime or text."
                )

        else:
            logger.warning("No <time> tag found for article at URL: %s", article_url)

        return article_date


if __name__ == "__main__":

    fetcher = YahooCryptoNewsScraper()
    raw_data = fetcher.fetch_news()
