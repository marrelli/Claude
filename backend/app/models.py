from sqlalchemy import Column, Integer, String, Text, DateTime, Float, Boolean, ForeignKey, Table, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()

# Association table for domains and articles (many-to-many)
article_domain_association = Table(
    'article_domain_association',
    Base.metadata,
    Column('article_id', Integer, ForeignKey('articles.id')),
    Column('domain_id', Integer, ForeignKey('domains.id'))
)


class Domain(Base):
    __tablename__ = 'domains'

    id = Column(Integer, primary_key=True)
    name = Column(String(255), unique=True, nullable=False)
    keywords = Column(JSON, nullable=True)  # List of keywords for matching
    active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    articles = relationship('Article', secondary=article_domain_association, back_populates='domains')


class Source(Base):
    __tablename__ = 'sources'

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    url = Column(String(500), nullable=False)
    source_type = Column(String(50), nullable=False)  # 'rss', 'api', 'custom'
    active = Column(Boolean, default=True)
    quality_score = Column(Float, default=5.0)
    thumbs_down_count = Column(Integer, default=0)
    last_used_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    articles = relationship('Article', back_populates='source')


class Article(Base):
    __tablename__ = 'articles'

    id = Column(Integer, primary_key=True)
    title = Column(String(500), nullable=False)
    content = Column(Text, nullable=True)
    original_url = Column(String(500), unique=True, nullable=False)
    source_id = Column(Integer, ForeignKey('sources.id'), nullable=False)

    summary = Column(Text, nullable=True)  # AI-generated summary
    contradictions = Column(JSON, nullable=True)  # AI-identified contradictions

    source_count = Column(Integer, default=1)  # How many sources report this
    source_list = Column(JSON, nullable=True)  # List of source IDs reporting this

    priority_score = Column(Float, default=0.0)

    created_at = Column(DateTime, default=datetime.utcnow)
    fetched_at = Column(DateTime, default=datetime.utcnow)

    source = relationship('Source', back_populates='articles')
    domains = relationship('Domain', secondary=article_domain_association, back_populates='articles')
    feedback_list = relationship('ArticleFeedback', back_populates='article', cascade='all, delete-orphan')


class SourceSuggestion(Base):
    __tablename__ = 'source_suggestions'

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    url = Column(String(500), nullable=False)
    description = Column(Text, nullable=True)
    status = Column(String(50), default='pending')  # 'pending', 'approved', 'rejected'
    suggested_at = Column(DateTime, default=datetime.utcnow)
    reviewed_at = Column(DateTime, nullable=True)


class ArticleFeedback(Base):
    __tablename__ = 'article_feedback'

    id = Column(Integer, primary_key=True)
    article_id = Column(Integer, ForeignKey('articles.id'), nullable=False)
    feedback_type = Column(String(50), nullable=False)  # 'heart', 'thumbs_up', 'thumbs_down'
    created_at = Column(DateTime, default=datetime.utcnow)

    article = relationship('Article', back_populates='feedback_list')


class Share(Base):
    __tablename__ = 'shares'

    id = Column(Integer, primary_key=True)
    article_id = Column(Integer, ForeignKey('articles.id'), nullable=False)
    unique_token = Column(String(255), unique=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    view_count = Column(Integer, default=0)
