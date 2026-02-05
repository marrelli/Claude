from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class DomainBase(BaseModel):
    name: str
    keywords: Optional[List[str]] = None


class DomainCreate(DomainBase):
    pass


class Domain(DomainBase):
    id: int
    active: bool
    created_at: datetime

    class Config:
        from_attributes = True


class SourceBase(BaseModel):
    name: str
    url: str
    source_type: str  # 'rss', 'api', 'custom'


class SourceCreate(SourceBase):
    pass


class Source(SourceBase):
    id: int
    active: bool
    quality_score: float
    thumbs_down_count: int
    last_used_at: Optional[datetime]
    created_at: datetime

    class Config:
        from_attributes = True


class SourceSuggestionBase(BaseModel):
    name: str
    url: str
    description: Optional[str] = None


class SourceSuggestionCreate(SourceSuggestionBase):
    pass


class SourceSuggestion(SourceSuggestionBase):
    id: int
    status: str
    suggested_at: datetime
    reviewed_at: Optional[datetime]

    class Config:
        from_attributes = True


class ArticleFeedbackBase(BaseModel):
    feedback_type: str  # 'heart', 'thumbs_up', 'thumbs_down'


class ArticleFeedbackCreate(ArticleFeedbackBase):
    pass


class ArticleFeedback(ArticleFeedbackBase):
    id: int
    article_id: int
    created_at: datetime

    class Config:
        from_attributes = True


class ShareBase(BaseModel):
    article_id: int


class Share(ShareBase):
    id: int
    unique_token: str
    created_at: datetime
    view_count: int

    class Config:
        from_attributes = True


class ArticleBase(BaseModel):
    title: str
    content: Optional[str] = None
    original_url: str
    source_id: int


class ArticleCreate(ArticleBase):
    pass


class Article(ArticleBase):
    id: int
    summary: Optional[str] = None
    contradictions: Optional[List[str]] = None
    source_count: int
    source_list: Optional[List[int]] = None
    priority_score: float
    created_at: datetime
    fetched_at: datetime
    source: Optional[Source] = None
    feedback_list: Optional[List[ArticleFeedback]] = None

    class Config:
        from_attributes = True


class ArticleWithDomains(Article):
    domains: Optional[List[Domain]] = None
