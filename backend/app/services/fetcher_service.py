import feedparser
import httpx
from datetime import datetime
import hashlib
from typing import List, Optional
from app.core.config import settings
import asyncio


class FetcherService:
    def __init__(self):
        self.http_client = httpx.Client(timeout=30.0)
        self.user_agent = "DailyNewsCuration/1.0 (Knowledge Curation Bot)"

    async def fetch_from_newsapi(self, keywords: str) -> List[dict]:
        """Fetch articles from NewsAPI."""
        if not settings.NEWS_API_KEY:
            return []

        articles = []
        try:
            url = "https://newsapi.org/v2/everything"
            params = {
                "q": keywords,
                "apiKey": settings.NEWS_API_KEY,
                "sortBy": "publishedAt",
                "language": "en",
                "pageSize": 10
            }

            response = self.http_client.get(url, params=params)
            response.raise_for_status()
            data = response.json()

            for item in data.get("articles", []):
                articles.append({
                    "title": item.get("title"),
                    "content": item.get("content") or item.get("description"),
                    "url": item.get("url"),
                    "source": item.get("source", {}).get("name"),
                    "published_at": item.get("publishedAt"),
                    "image": item.get("urlToImage")
                })
        except Exception as e:
            print(f"Error fetching from NewsAPI: {e}")

        return articles

    async def fetch_from_rss(self, feed_url: str) -> List[dict]:
        """Fetch articles from RSS feed."""
        articles = []
        try:
            feed = feedparser.parse(feed_url)

            for entry in feed.entries[:10]:
                articles.append({
                    "title": entry.get("title"),
                    "content": entry.get("summary") or entry.get("description"),
                    "url": entry.get("link"),
                    "source": feed.feed.get("title", "RSS Feed"),
                    "published_at": entry.get("published", str(datetime.utcnow())),
                })
        except Exception as e:
            print(f"Error fetching from RSS {feed_url}: {e}")

        return articles

    async def fetch_from_reddit(self, subreddit: str) -> List[dict]:
        """Fetch discussions from Reddit."""
        articles = []
        try:
            url = f"https://www.reddit.com/r/{subreddit}/hot.json"
            headers = {"User-Agent": self.user_agent}

            response = self.http_client.get(url, headers=headers)
            response.raise_for_status()
            data = response.json()

            for post in data.get("data", {}).get("children", [])[:10]:
                post_data = post.get("data", {})
                articles.append({
                    "title": post_data.get("title"),
                    "content": post_data.get("selftext") or post_data.get("url"),
                    "url": f"https://reddit.com{post_data.get('permalink')}",
                    "source": f"Reddit r/{subreddit}",
                    "published_at": str(datetime.fromtimestamp(post_data.get("created_utc")))
                })
        except Exception as e:
            print(f"Error fetching from Reddit: {e}")

        return articles

    def deduplicate_articles(self, articles: List[dict]) -> dict:
        """Group similar articles and detect duplicates."""
        grouped = {}

        for article in articles:
            # Create a hash of the content to detect duplicates
            content_hash = hashlib.md5(
                (article.get("title", "") + article.get("content", "")).encode()
            ).hexdigest()

            if content_hash not in grouped:
                grouped[content_hash] = {
                    "title": article.get("title"),
                    "content": article.get("content"),
                    "url": article.get("url"),
                    "published_at": article.get("published_at"),
                    "sources": []
                }

            grouped[content_hash]["sources"].append({
                "name": article.get("source"),
                "original_url": article.get("url")
            })

        return grouped

    async def fetch_all_sources(self, domains: List[dict]) -> List[dict]:
        """Fetch articles from all configured sources."""
        all_articles = []

        for domain in domains:
            keywords = " OR ".join(domain.get("keywords", [domain.get("name")]))

            # Fetch from NewsAPI
            articles = await self.fetch_from_newsapi(keywords)
            all_articles.extend(articles)

        return all_articles

    def close(self):
        """Close HTTP client."""
        self.http_client.close()
