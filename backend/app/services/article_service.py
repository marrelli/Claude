from sqlalchemy.orm import Session
from sqlalchemy import and_, desc, func
from app.models import Article, Source, Domain, ArticleFeedback
from app.schemas import ArticleCreate
from datetime import datetime, timedelta
import uuid
from typing import List, Optional
from difflib import SequenceMatcher


class ArticleService:
    def __init__(self, db: Session):
        self.db = db

    def calculate_priority_score(
        self,
        source_count: int,
        domain_relevance: float = 0.5,  # 0.0-1.0
        freshness_hours: float = 1.0,   # hours since published
        engagement_score: float = 0.0   # based on feedback
    ) -> float:
        """Calculate priority score for article ranking."""
        # Normalize freshness (more recent = higher score)
        freshness_factor = max(0, 1.0 - (freshness_hours / 24.0))

        priority = (
            source_count * 0.4 +
            domain_relevance * 0.3 +
            freshness_factor * 0.2 +
            engagement_score * 0.1
        )

        return priority

    def find_matching_domains(self, article_title: str, article_content: str) -> List[int]:
        """Find which domains match this article."""
        domains = self.db.query(Domain).filter(Domain.active == True).all()
        matched_domain_ids = []

        article_text = (article_title + " " + (article_content or "")).lower()

        for domain in domains:
            keywords = domain.keywords or [domain.name.lower()]
            if any(keyword.lower() in article_text for keyword in keywords):
                matched_domain_ids.append(domain.id)

        return matched_domain_ids if matched_domain_ids else [domains[0].id] if domains else []

    def find_duplicate_article(self, title: str, url: str) -> Optional[Article]:
        """Find if article already exists (by URL or similar title)."""
        # Check by URL first
        existing = self.db.query(Article).filter(Article.original_url == url).first()
        if existing:
            return existing

        return None

    def merge_article_sources(self, article: Article, new_source_id: int) -> None:
        """Merge a new source into an existing article."""
        if article.source_list is None:
            article.source_list = [article.source_id]

        if new_source_id not in article.source_list:
            article.source_list.append(new_source_id)

        article.source_count = len(article.source_list)
        self.db.commit()

    def create_article(
        self,
        title: str,
        content: str,
        url: str,
        source_id: int,
        summary: Optional[str] = None,
        contradictions: Optional[dict] = None
    ) -> Article:
        """Create a new article."""
        # Check for duplicates
        existing = self.find_duplicate_article(title, url)
        if existing:
            self.merge_article_sources(existing, source_id)
            return existing

        # Find matching domains
        domain_ids = self.find_matching_domains(title, content)

        # Calculate initial priority
        freshness_hours = 0
        priority = self.calculate_priority_score(
            source_count=1,
            domain_relevance=1.0 if domain_ids else 0.3,
            freshness_hours=freshness_hours
        )

        article = Article(
            title=title,
            content=content,
            original_url=url,
            source_id=source_id,
            summary=summary,
            contradictions=contradictions,
            source_count=1,
            source_list=[source_id],
            priority_score=priority
        )

        # Add domain associations
        domains = self.db.query(Domain).filter(Domain.id.in_(domain_ids)).all()
        for domain in domains:
            article.domains.append(domain)

        self.db.add(article)
        self.db.commit()
        self.db.refresh(article)

        return article

    def get_articles_feed(
        self,
        domain_id: Optional[int] = None,
        limit: int = 20,
        offset: int = 0
    ) -> tuple[List[Article], int]:
        """Get articles for dashboard, ordered by priority."""
        query = self.db.query(Article)

        if domain_id:
            query = query.join(Article.domains).filter(Domain.id == domain_id)

        # Order by priority score (highest first)
        query = query.order_by(desc(Article.priority_score), desc(Article.created_at))

        total = query.count()
        articles = query.limit(limit).offset(offset).all()

        return articles, total

    def update_priority_scores(self) -> None:
        """Recalculate priority scores for all articles (run periodically)."""
        articles = self.db.query(Article).all()
        now = datetime.utcnow()

        for article in articles:
            freshness_hours = (now - article.created_at).total_seconds() / 3600

            # Calculate engagement score from feedback
            hearts = self.db.query(func.count(ArticleFeedback.id)).filter(
                and_(
                    ArticleFeedback.article_id == article.id,
                    ArticleFeedback.feedback_type.in_(["heart", "thumbs_up"])
                )
            ).scalar() or 0

            thumbs_down = self.db.query(func.count(ArticleFeedback.id)).filter(
                and_(
                    ArticleFeedback.article_id == article.id,
                    ArticleFeedback.feedback_type == "thumbs_down"
                )
            ).scalar() or 0

            engagement_score = (hearts - thumbs_down) / max(1, hearts + thumbs_down)

            # Domain relevance (how many domains it matches)
            domain_count = len(article.domains)
            total_domains = self.db.query(Domain).filter(Domain.active == True).count()
            domain_relevance = domain_count / max(1, total_domains)

            article.priority_score = self.calculate_priority_score(
                source_count=article.source_count,
                domain_relevance=domain_relevance,
                freshness_hours=freshness_hours,
                engagement_score=max(-1, min(1, engagement_score))  # Clamp to [-1, 1]
            )

        self.db.commit()

    def add_feedback(self, article_id: int, feedback_type: str) -> None:
        """Add feedback (heart, thumbs_up, thumbs_down) to an article."""
        article = self.db.query(Article).filter(Article.id == article_id).first()
        if not article:
            return

        feedback = ArticleFeedback(article_id=article_id, feedback_type=feedback_type)
        self.db.add(feedback)

        # Update source quality if thumbs_down
        if feedback_type == "thumbs_down":
            source = self.db.query(Source).filter(Source.id == article.source_id).first()
            if source:
                source.thumbs_down_count += 1
                source.quality_score = max(1.0, source.quality_score - 0.2)

                # Auto-remove source if too many thumbs down
                if source.thumbs_down_count > 5:
                    source.active = False

        self.db.commit()

    def remove_old_articles(self, days: int = 30) -> int:
        """Remove articles older than specified days."""
        cutoff_date = datetime.utcnow() - timedelta(days=days)
        deleted = self.db.query(Article).filter(Article.created_at < cutoff_date).delete()
        self.db.commit()
        return deleted
