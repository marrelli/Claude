from sqlalchemy.orm import Session
from app.models import Share, Article
from typing import Optional
import uuid


class ShareService:
    def __init__(self, db: Session):
        self.db = db

    def create_share(self, article_id: int) -> Optional[Share]:
        """Create a shareable link for an article."""
        article = self.db.query(Article).filter(Article.id == article_id).first()
        if not article:
            return None

        # Check if share already exists
        existing_share = self.db.query(Share).filter(Share.article_id == article_id).first()
        if existing_share:
            return existing_share

        # Create new share with unique token
        unique_token = str(uuid.uuid4())
        share = Share(
            article_id=article_id,
            unique_token=unique_token
        )

        self.db.add(share)
        self.db.commit()
        self.db.refresh(share)

        return share

    def get_share_by_token(self, token: str) -> Optional[Share]:
        """Retrieve share by unique token."""
        share = self.db.query(Share).filter(Share.unique_token == token).first()
        if share:
            # Increment view count
            share.view_count += 1
            self.db.commit()

        return share

    def get_article_from_share(self, token: str) -> Optional[Article]:
        """Get the article associated with a share token."""
        share = self.get_share_by_token(token)
        if share:
            return self.db.query(Article).filter(Article.id == share.article_id).first()
        return None

    def delete_share(self, share_id: int) -> bool:
        """Delete a share link."""
        share = self.db.query(Share).filter(Share.id == share_id).first()
        if share:
            self.db.delete(share)
            self.db.commit()
            return True
        return False
