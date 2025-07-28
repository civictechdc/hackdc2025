"""Pydantic models for the application."""
from typing import Optional, Set
from pydantic import BaseModel, Field

class DocketBase(BaseModel):
    """Base class for Docket models."""
    title: str
    summary: str

class DocketCreate(DocketBase):
    """Model for creating a new Docket."""
    docket_id: int

class DocketUpdate(DocketBase):
    """Model for updating an existing Docket."""
    title: Optional[str] = None
    summary: Optional[str] = None

class Docket(DocketBase):
    """Docket model with all fields."""
    docket_id: int
    keywords: Optional[Set[str]] = None
    
    class Config:
        """Pydantic configuration."""
        from_attributes = True  # For SQLAlchemy compatibility
