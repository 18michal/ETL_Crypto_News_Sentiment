Project:
# Bitcoin Social Media Sentiment Analysis project with an ETL/ELT process.
## Project Overview

This project involves building an ETL/ELT pipeline to extract cryptocurrency-related news articles, process the text using machine learning models for sentiment analysis, and load the results into an Azure SQL Database for storage. The goal is to analyze social media sentiment and categorize cryptocurrency news into three sentiment classes: Positive, Neutral, and Negative.

The pipeline is fully automated, designed to run on a schedule to scrape, preprocess, classify, and load data.

## Features
- **Data Extraction**: Scrapes cryptocurrency news articles from [Yahoo Finance](https://finance.yahoo.com/topic/crypto/)
- **Data Transformation**: Preprocesses the articles and applies sentiment analysis using a trained machine learning model.
- **Data Loading**: Loads the transformed data into an **Azure SQL Database**.
- **Custom Machine Learning Models**: Includes models for sentiment analysis using TF-IDF vectorization and deep learning techniques.


## Folder Structure

src/<br> ├── ml_models/<br> │ ├── crypto_sentiment_model/<br> │ ├── crypto_sentiment_modeltfidf_vectorizer/<br> ├── nltk_data/<br> ├── db_utils_helper.py<br> ├── fetch_news.py<br> ├── load_news.py<br> ├── project_config.py<br> ├── transform_news.py<br> app.p<br> .gitignore<br> .env<br> poetry.lock<br> poetry.toml<br> README.md


### `src/`
- **ml_models/**: Contains machine learning models used for sentiment analysis.
- **nltk_data/**: Stores necessary NLTK data files for text preprocessing.
- **db_utils_helper.py**: Provides utility functions for interacting with the database.
- **fetch_news.py**: Scrapes cryptocurrency news articles.
- **load_news.py**: Loads processed data into the Azure SQL Database.
- **project_config.py**: Configuration file for database connection and other settings.
- **transform_news.py**: Transforms raw data into the format suitable for machine learning models.

### `app.py`
- The main script that runs the ETL process: fetching, transforming, and loading data.

### `.env`
- Contains environment variables for database credentials and configuration settings.
**Note**: It’s recommended to use **Azure Key Vault** for production environments, but for this project, you can use local environment variables for simplicity.
`DB_SERVER=your_database_server`
`DB_NAME=your_database_name`
`DB_USER=your_database_user`
`DB_PASSWORD=your_database_password`


It would be better to use Azure Key Vault but it is paid so i prefer to use local environemnt

### `poetry.toml` & `poetry.lock`
- Configuration files for managing Python dependencies using Poetry.
