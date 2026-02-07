from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas import Article, ArticleWithDomains
from app.services.article_service import ArticleService
from app.services.fetcher_service import FetcherService
from app.services.ai_service import AIService
from app.services.domain_service import DomainService
from typing import List
import asyncio

router = APIRouter(prefix="/articles", tags=["articles"])


@router.get("/feed", response_model=dict)
async def get_articles_feed(
    domain_id: int = Query(None),
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db)
):
    """Get prioritized articles feed."""
    article_service = ArticleService(db)
    articles, total = article_service.get_articles_feed(domain_id, limit, offset)

    # Convert SQLAlchemy models to Pydantic schemas
    articles_data = [
        {
            "id": a.id,
            "title": a.title,
            "content": a.content,
            "original_url": a.original_url,
            "summary": a.summary,
            "contradictions": a.contradictions,
            "source_count": a.source_count,
            "source_list": a.source_list,
            "priority_score": a.priority_score,
            "created_at": a.created_at,
            "fetched_at": a.fetched_at,
            "source": {"id": a.source.id, "name": a.source.name, "url": a.source.url, "source_type": a.source.source_type} if a.source else None,
            "domains": [{"id": d.id, "name": d.name, "keywords": d.keywords, "active": d.active, "created_at": d.created_at} for d in a.domains]
        }
        for a in articles
    ]

    return {
        "articles": articles_data,
        "total": total,
        "limit": limit,
        "offset": offset
    }


@router.post("/feedback/{article_id}")
async def add_article_feedback(
    article_id: int,
    feedback_type: str = Query(..., description="heart, thumbs_up, or thumbs_down"),
    db: Session = Depends(get_db)
):
    """Add feedback to an article."""
    if feedback_type not in ["heart", "thumbs_up", "thumbs_down"]:
        raise HTTPException(status_code=400, detail="Invalid feedback type")

    article_service = ArticleService(db)
    article_service.add_feedback(article_id, feedback_type)

    return {"status": "success", "feedback_type": feedback_type}


@router.post("/fetch-now")
async def fetch_new_articles(db: Session = Depends(get_db)):
    """Manually trigger article fetch from all sources."""
    try:
        domain_service = DomainService(db)
        fetcher_service = FetcherService()
        ai_service = AIService()
        article_service = ArticleService(db)

        domains = domain_service.get_all_domains()
        if not domains:
            domains = domain_service.get_default_domains()

        # Fetch articles
        all_articles = await fetcher_service.fetch_all_sources(
            [{"name": d.name, "keywords": d.keywords} for d in domains]
        )

        # Deduplicate
        deduplicated = fetcher_service.deduplicate_articles(all_articles)

        # Process articles
        articles_added = 0
        for content_hash, article_data in deduplicated.items():
            # Quality check
            if not ai_service.assess_content_quality(
                article_data["title"],
                article_data["content"]
            ):
                continue

            # Generate summary
            summary = ai_service.summarize_article(
                article_data["title"],
                article_data["content"]
            )

            # Get or create source (use first source for now)
            from app.services.source_service import SourceService
            source_service = SourceService(db)
            sources = source_service.get_all_sources()
            source_id = sources[0].id if sources else None

            if not source_id:
                continue

            # Create article
            article_service.create_article(
                title=article_data["title"],
                content=article_data["content"],
                url=article_data["url"],
                source_id=source_id,
                summary=summary
            )

            articles_added += 1

        # Recalculate priorities
        article_service.update_priority_scores()

        fetcher_service.close()

        return {
            "status": "success",
            "articles_found": len(deduplicated),
            "articles_added": articles_added,
            "message": f"Fetched {articles_added} new articles from {len(deduplicated)} total found"
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{article_id}", response_model=ArticleWithDomains)
async def get_article(article_id: int, db: Session = Depends(get_db)):
    """Get a specific article."""
    from app.models import Article
    article = db.query(Article).filter(Article.id == article_id).first()

    if not article:
        raise HTTPException(status_code=404, detail="Article not found")

    return article
