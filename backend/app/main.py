from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.database import init_db
from app.core.config import settings
from app.api import articles, domains, sources, shares
from app.services.scheduler_service import SchedulerService
from app.services.fetcher_service import FetcherService
from app.services.ai_service import AIService
from app.services.domain_service import DomainService
from app.services.article_service import ArticleService
from app.services.source_service import SourceService
from app.core.database import SessionLocal
import asyncio

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Daily news curation and continuous learning platform"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify allowed origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(articles.router)
app.include_router(domains.router)
app.include_router(sources.router)
app.include_router(shares.router)

# Initialize scheduler
scheduler_service = SchedulerService()


def scheduled_fetch():
    """Function to be called on schedule."""
    try:
        db = SessionLocal()

        domain_service = DomainService(db)
        fetcher_service = FetcherService()
        ai_service = AIService()
        article_service = ArticleService(db)
        source_service = SourceService(db)

        domains = domain_service.get_all_domains()
        if not domains:
            domains = domain_service.get_default_domains()

        # Fetch articles
        all_articles = asyncio.run(fetcher_service.fetch_all_sources(
            [{"name": d.name, "keywords": d.keywords} for d in domains]
        ))

        # Deduplicate
        deduplicated = fetcher_service.deduplicate_articles(all_articles)

        articles_added = 0
        for content_hash, article_data in deduplicated.items():
            # Quality check
            try:
                if not ai_service.assess_content_quality(
                    article_data["title"],
                    article_data["content"]
                ):
                    continue
            except Exception as e:
                print(f"Error assessing quality: {e}")
                continue

            # Generate summary
            try:
                summary = ai_service.summarize_article(
                    article_data["title"],
                    article_data["content"]
                )
            except Exception as e:
                print(f"Error summarizing: {e}")
                summary = None

            # Get primary source
            sources_list = source_service.get_all_sources()
            source_id = sources_list[0].id if sources_list else None

            if not source_id:
                continue

            # Create article
            try:
                article_service.create_article(
                    title=article_data["title"],
                    content=article_data["content"],
                    url=article_data["url"],
                    source_id=source_id,
                    summary=summary
                )
                articles_added += 1
            except Exception as e:
                print(f"Error creating article: {e}")
                continue

        # Recalculate priorities
        article_service.update_priority_scores()

        # Clean up old articles
        removed = article_service.remove_old_articles(days=30)

        fetcher_service.close()
        db.close()

        print(f"Scheduled fetch completed: {articles_added} articles added, {removed} old articles removed")

    except Exception as e:
        print(f"Error in scheduled fetch: {e}")


@app.on_event("startup")
async def startup_event():
    """Initialize database and start scheduler."""
    init_db()

    # Initialize default domains and sources
    db = SessionLocal()
    domain_service = DomainService(db)
    source_service = SourceService(db)

    domain_service.get_default_domains()
    source_service.get_default_sources()

    db.close()

    # Start scheduler
    scheduler_service.start(scheduled_fetch)


@app.on_event("shutdown")
async def shutdown_event():
    """Stop scheduler on shutdown."""
    scheduler_service.stop()


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION
    }


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": f"Welcome to {settings.APP_NAME}",
        "version": settings.APP_VERSION,
        "docs": "/docs"
    }
