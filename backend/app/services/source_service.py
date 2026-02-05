from sqlalchemy.orm import Session
from app.models import Source, SourceSuggestion
from app.schemas import SourceCreate, SourceSuggestionCreate
from typing import List, Optional
from datetime import datetime


class SourceService:
    def __init__(self, db: Session):
        self.db = db

    def create_source(self, source: SourceCreate) -> Source:
        """Create a new source."""
        db_source = Source(
            name=source.name,
            url=source.url,
            source_type=source.source_type,
            active=True,
            quality_score=5.0
        )
        self.db.add(db_source)
        self.db.commit()
        self.db.refresh(db_source)
        return db_source

    def get_all_sources(self) -> List[Source]:
        """Get all active sources."""
        return self.db.query(Source).filter(Source.active == True).all()

    def get_source(self, source_id: int) -> Optional[Source]:
        """Get a specific source by ID."""
        return self.db.query(Source).filter(Source.id == source_id).first()

    def delete_source(self, source_id: int) -> bool:
        """Soft delete a source (mark as inactive)."""
        source = self.get_source(source_id)
        if source:
            source.active = False
            self.db.commit()
            return True
        return False

    def suggest_source(self, suggestion: SourceSuggestionCreate) -> SourceSuggestion:
        """Store a source suggestion for curation."""
        db_suggestion = SourceSuggestion(
            name=suggestion.name,
            url=suggestion.url,
            description=suggestion.description,
            status="pending"
        )
        self.db.add(db_suggestion)
        self.db.commit()
        self.db.refresh(db_suggestion)
        return db_suggestion

    def get_all_suggestions(self) -> List[SourceSuggestion]:
        """Get all source suggestions."""
        return self.db.query(SourceSuggestion).all()

    def get_suggestions_by_status(self, status: str) -> List[SourceSuggestion]:
        """Get suggestions by status (pending, approved, rejected)."""
        return self.db.query(SourceSuggestion).filter(SourceSuggestion.status == status).all()

    def approve_suggestion(self, suggestion_id: int) -> Optional[Source]:
        """Approve a suggestion and create a source from it."""
        suggestion = self.db.query(SourceSuggestion).filter(
            SourceSuggestion.id == suggestion_id
        ).first()

        if not suggestion:
            return None

        # Check if source already exists
        existing = self.db.query(Source).filter(Source.url == suggestion.url).first()
        if existing:
            suggestion.status = "approved"
            suggestion.reviewed_at = datetime.utcnow()
            self.db.commit()
            return existing

        # Create new source
        source = Source(
            name=suggestion.name,
            url=suggestion.url,
            source_type="custom",
            active=True,
            quality_score=5.0
        )
        self.db.add(source)

        suggestion.status = "approved"
        suggestion.reviewed_at = datetime.utcnow()

        self.db.commit()
        self.db.refresh(source)

        return source

    def reject_suggestion(self, suggestion_id: int) -> bool:
        """Reject a source suggestion."""
        suggestion = self.db.query(SourceSuggestion).filter(
            SourceSuggestion.id == suggestion_id
        ).first()

        if suggestion:
            suggestion.status = "rejected"
            suggestion.reviewed_at = datetime.utcnow()
            self.db.commit()
            return True

        return False

    def get_default_sources(self) -> List[Source]:
        """Initialize default sources."""
        default_sources = [
            {
                "name": "NewsAPI",
                "url": "https://newsapi.org",
                "type": "api"
            },
            {
                "name": "TechCrunch",
                "url": "https://feeds.techcrunch.com/feed",
                "type": "rss"
            },
            {
                "name": "Hacker News",
                "url": "https://news.ycombinator.com/",
                "type": "custom"
            },
            {
                "name": "The Verge",
                "url": "https://www.theverge.com/rss/index.xml",
                "type": "rss"
            }
        ]

        sources = []
        for source_data in default_sources:
            existing = self.db.query(Source).filter(
                Source.url == source_data["url"]
            ).first()
            if not existing:
                new_source = Source(
                    name=source_data["name"],
                    url=source_data["url"],
                    source_type=source_data["type"],
                    active=True,
                    quality_score=5.0
                )
                self.db.add(new_source)
                sources.append(new_source)

        self.db.commit()

        # Return all (new + existing)
        return self.db.query(Source).filter(Source.active == True).all()
