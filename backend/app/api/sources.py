from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas import Source, SourceCreate, SourceSuggestion, SourceSuggestionCreate
from app.services.source_service import SourceService
from typing import List

router = APIRouter(prefix="/sources", tags=["sources"])


@router.get("", response_model=dict)
async def get_sources(db: Session = Depends(get_db)):
    """Get all sources and suggestions."""
    source_service = SourceService(db)

    sources = source_service.get_all_sources()
    if not sources:
        # Initialize with defaults
        sources = source_service.get_default_sources()

    suggestions = source_service.get_all_suggestions()

    return {
        "sources": sources,
        "suggestions": suggestions
    }


@router.post("", response_model=Source)
async def create_source(source: SourceCreate, db: Session = Depends(get_db)):
    """Create a new source."""
    source_service = SourceService(db)

    # Check if source already exists
    from app.models import Source as SourceModel
    existing = db.query(SourceModel).filter(SourceModel.url == source.url).first()
    if existing:
        raise HTTPException(status_code=400, detail="Source already exists")

    return source_service.create_source(source)


@router.delete("/{source_id}")
async def delete_source(source_id: int, db: Session = Depends(get_db)):
    """Delete a source."""
    source_service = SourceService(db)

    if not source_service.delete_source(source_id):
        raise HTTPException(status_code=404, detail="Source not found")

    return {"status": "success", "message": "Source deleted"}


@router.post("/suggest", response_model=SourceSuggestion)
async def suggest_source(
    suggestion: SourceSuggestionCreate,
    db: Session = Depends(get_db)
):
    """Suggest a new source."""
    source_service = SourceService(db)
    return source_service.suggest_source(suggestion)


@router.get("/suggestions/pending", response_model=List[SourceSuggestion])
async def get_pending_suggestions(db: Session = Depends(get_db)):
    """Get all pending source suggestions."""
    source_service = SourceService(db)
    return source_service.get_suggestions_by_status("pending")


@router.post("/suggestions/{suggestion_id}/approve", response_model=Source)
async def approve_suggestion(suggestion_id: int, db: Session = Depends(get_db)):
    """Approve a source suggestion."""
    source_service = SourceService(db)
    source = source_service.approve_suggestion(suggestion_id)

    if not source:
        raise HTTPException(status_code=404, detail="Suggestion not found")

    return source


@router.post("/suggestions/{suggestion_id}/reject")
async def reject_suggestion(suggestion_id: int, db: Session = Depends(get_db)):
    """Reject a source suggestion."""
    source_service = SourceService(db)

    if not source_service.reject_suggestion(suggestion_id):
        raise HTTPException(status_code=404, detail="Suggestion not found")

    return {"status": "success", "message": "Suggestion rejected"}
