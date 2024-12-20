import logging
import os
from datetime import datetime
from typing import Any, Optional

import joblib
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize

from src.project_config import YahooConfig

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(funcName)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


class CryptoNewsTransformer(YahooConfig):
    """Transform and classify cryptocurrency news data."""

    def __init__(self) -> None:
        super().__init__()
        self.setup_nltk()
        self.model: Any = self._load_model(model_path=self.PATH_SENTIMENT_MODEL)
        self.vectorizer: Any = self._load_model(
            model_path=self.PATH_SENTIMENT__VECTORIZER
        )

    def transform_news(self, raw_data: list[dict[str, Optional[str]]]) -> list[dict]:
        """Preprocess and classify the sentiment of news articles."""
        # Remove articles where something is None
        data: list[dict] = [
            {key: (value if value is not None else "") for key, value in item.items()}
            for item in raw_data
            if item["content"] is not None
        ]

        # Convert date to datetime
        data = list(map(self._parse_date, data))

        # Process and classify sentiment
        for article in data:
            article["preprocessed_content"] = self._preprocess_content(
                text=article["content"]
            )
            article["sentiment"] = self._classify_sentiment_for_atticle(
                text_preprocessed=article["preprocessed_content"]
            )

        logger.info("Data cleaned and sucessfully clasified.")
        return data

    def setup_nltk(self) -> None:
        """Set up NLTK resources."""
        nltk_data_path = os.path.join(os.path.dirname(__file__), self.FOLDER_NLTK_DATA)
        os.makedirs(nltk_data_path, exist_ok=True)
        nltk.data.path.append(nltk_data_path)

        required_nltk_resources = ["stopwords", "wordnet", "punkt_tab"]
        for resource in required_nltk_resources:
            try:
                (
                    nltk.data.find(f"tokenizers/{resource}")
                    if resource == "punkt_tab"
                    else nltk.data.find(f"corpora/{resource}")
                )
            except LookupError:
                nltk.download(resource, download_dir=nltk_data_path)

        logger.info("nltk resources loaded.")

    def _parse_date(self, item: dict[str, str]) -> dict:
        """Convert date to datetime object."""
        return {
            **item,  # all fields except "date" are copied as-is.
            "date": (
                datetime.strptime(item["date"], "%Y-%m-%dT%H:%M:%S.%fZ")
                if item["date"]
                else None
            ),
        }

    def _preprocess_content(self, text: str) -> str:
        """Preprocess the text for sentiment classification."""
        lemmatizer = WordNetLemmatizer()
        stop_words = set(stopwords.words("english"))
        word_tokens = word_tokenize(text.lower())
        processed_text = [
            lemmatizer.lemmatize(word)
            for word in word_tokens
            if word.isalnum() and word not in stop_words
        ]
        return " ".join(processed_text)

    def _classify_sentiment_for_atticle(self, text_preprocessed: str) -> str:
        """Classify the sentiment of the article content."""
        transformed_text = self.vectorizer.transform([text_preprocessed])
        prediction = self.model.predict(transformed_text)
        return prediction[0]

    def _load_model(self, model_path: str) -> Any:
        """Load the pre-trained model"""
        try:
            model_path = os.path.join(os.path.dirname(__file__), model_path)
            if model_path:
                return joblib.load(model_path)
        except FileNotFoundError as e:
            logger.error("Failed to load sentiment model: %s", str(e))
            raise
        except Exception as e:
            logger.error("An unexpected error occurred: %s", str(e))
            raise
