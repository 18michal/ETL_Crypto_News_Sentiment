class YahooConfig:
    """
    Configuration class to store settings related to the cryptocurrency news scraper.
    """

    URL = "https://finance.yahoo.com/topic/crypto/"
    ARTICLE_UNWANTED_CONTENT_START = [
        "News",
        "Life",
        "Entertainment",
        "Finance",
        "Sports",
        "New on Yahoo",
        "Yahoo Finance",
        "We are experiencing some temporary issues.",
        "The market data on this page is currently delayed.",
        "Please bear with us as we address this and restore your personalized lists.",
    ]
    ARTICLE_UNWANTED_CONTENT_END = [
        "Recommended Stories",
        "Sign in to access your portfolio",
    ]
