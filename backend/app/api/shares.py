from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas import Share, ArticleWithDomains
from app.services.share_service import ShareService

router = APIRouter(prefix="/share", tags=["sharing"])


@router.post("/{article_id}", response_model=Share)
async def create_share(article_id: int, db: Session = Depends(get_db)):
    """Create a shareable link for an article."""
    share_service = ShareService(db)
    share = share_service.create_share(article_id)

    if not share:
        raise HTTPException(status_code=404, detail="Article not found")

    return share


@router.get("/{token}", response_model=dict)
async def get_shared_article(token: str, db: Session = Depends(get_db)):
    """Get a shared article by token (public endpoint)."""
    share_service = ShareService(db)
    article = share_service.get_article_from_share(token)

    if not article:
        raise HTTPException(status_code=404, detail="Share not found")

    return {
        "article": article,
        "token": token
    }


@router.delete("/{share_id}")
async def delete_share(share_id: int, db: Session = Depends(get_db)):
    """Delete a shareable link."""
    share_service = ShareService(db)

    if not share_service.delete_share(share_id):
        raise HTTPException(status_code=404, detail="Share not found")

    return {"status": "success", "message": "Share deleted"}
