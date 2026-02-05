from sqlalchemy.orm import Session
from app.models import Domain
from app.schemas import DomainCreate
from typing import List, Optional


class DomainService:
    def __init__(self, db: Session):
        self.db = db

    def create_domain(self, domain: DomainCreate) -> Domain:
        """Create a new domain."""
        db_domain = Domain(
            name=domain.name,
            keywords=domain.keywords or [domain.name.lower()],
            active=True
        )
        self.db.add(db_domain)
        self.db.commit()
        self.db.refresh(db_domain)
        return db_domain

    def get_all_domains(self) -> List[Domain]:
        """Get all active domains."""
        return self.db.query(Domain).filter(Domain.active == True).all()

    def get_domain(self, domain_id: int) -> Optional[Domain]:
        """Get a specific domain by ID."""
        return self.db.query(Domain).filter(Domain.id == domain_id).first()

    def update_domain(self, domain_id: int, name: str, keywords: List[str]) -> Optional[Domain]:
        """Update a domain."""
        domain = self.get_domain(domain_id)
        if domain:
            domain.name = name
            domain.keywords = keywords or [name.lower()]
            self.db.commit()
            self.db.refresh(domain)
        return domain

    def delete_domain(self, domain_id: int) -> bool:
        """Soft delete a domain (mark as inactive)."""
        domain = self.get_domain(domain_id)
        if domain:
            domain.active = False
            self.db.commit()
            return True
        return False

    def get_default_domains(self) -> List[Domain]:
        """Initialize default domains if they don't exist."""
        default_domains = [
            "Technology Industry",
            "Artificial Intelligence",
            "Future of Work",
            "Entertainment and Media Industry",
            "Data Management"
        ]

        domains = []
        for domain_name in default_domains:
            existing = self.db.query(Domain).filter(Domain.name == domain_name).first()
            if not existing:
                new_domain = Domain(
                    name=domain_name,
                    keywords=[domain_name.lower(), domain_name.split()[0].lower()],
                    active=True
                )
                self.db.add(new_domain)
                domains.append(new_domain)

        self.db.commit()

        # Return all (new + existing)
        return self.db.query(Domain).filter(Domain.active == True).all()
