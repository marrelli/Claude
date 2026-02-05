from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas import Domain, DomainCreate
from app.services.domain_service import DomainService
from typing import List

router = APIRouter(prefix="/domains", tags=["domains"])


@router.get("", response_model=List[Domain])
async def get_domains(db: Session = Depends(get_db)):
    """Get all active domains."""
    domain_service = DomainService(db)
    domains = domain_service.get_all_domains()

    if not domains:
        # Initialize with defaults
        domains = domain_service.get_default_domains()

    return domains


@router.post("", response_model=Domain)
async def create_domain(domain: DomainCreate, db: Session = Depends(get_db)):
    """Create a new domain."""
    domain_service = DomainService(db)

    # Check if domain already exists
    existing = db.query(Domain).filter(Domain.name == domain.name).first()
    if existing:
        raise HTTPException(status_code=400, detail="Domain already exists")

    return domain_service.create_domain(domain)


@router.delete("/{domain_id}")
async def delete_domain(domain_id: int, db: Session = Depends(get_db)):
    """Delete a domain."""
    domain_service = DomainService(db)

    if not domain_service.delete_domain(domain_id):
        raise HTTPException(status_code=404, detail="Domain not found")

    return {"status": "success", "message": "Domain deleted"}


@router.put("/{domain_id}", response_model=Domain)
async def update_domain(
    domain_id: int,
    name: str,
    keywords: list = None,
    db: Session = Depends(get_db)
):
    """Update a domain."""
    domain_service = DomainService(db)
    updated = domain_service.update_domain(domain_id, name, keywords)

    if not updated:
        raise HTTPException(status_code=404, detail="Domain not found")

    return updated
