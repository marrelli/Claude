import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    # Database
    DATABASE_URL = os.getenv(
        "DATABASE_URL",
        "postgresql://user:password@localhost:5432/daily_news_db"
    )

    # API Keys
    ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
    NEWS_API_KEY = os.getenv("NEWS_API_KEY")
    TWITTER_API_KEY = os.getenv("TWITTER_API_KEY")
    TWITTER_API_SECRET = os.getenv("TWITTER_API_SECRET")
    TWITTER_BEARER_TOKEN = os.getenv("TWITTER_BEARER_TOKEN")

    # App Settings
    APP_NAME = "Daily News Curation"
    APP_VERSION = "0.1.0"
    DEBUG = os.getenv("DEBUG", "False") == "True"

    # Fetch Schedule (Eastern Time)
    FETCH_TIMES = ["05:00", "17:00"]  # 5am and 5pm ET

    # AI Model
    DEFAULT_AI_MODEL = "claude-3-5-sonnet-20241022"

    # API Pagination
    ARTICLES_PER_PAGE = 20


settings = Settings()
