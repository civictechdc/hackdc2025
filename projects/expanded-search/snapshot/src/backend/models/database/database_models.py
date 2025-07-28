"""SQLAlchemy database models."""
from sqlalchemy import Column, Integer, String, ForeignKey, Table, UniqueConstraint
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

# Association table for many-to-many relationship between dockets and keywords
docket_keywords = Table(
    "docket_keywords",
    Base.metadata,
    Column("docket_id", Integer, ForeignKey("dockets.docket_id"), primary_key=True),
    Column("keyword_id", Integer, ForeignKey("keywords.id"), primary_key=True),
    UniqueConstraint("docket_id", "keyword_id", name="uq_docket_keyword"),
)

class DocketModel(Base):
    """SQLAlchemy model for dockets."""
    __tablename__ = "dockets"

    docket_id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    summary = Column(String, nullable=False)
    
    # Relationship with keywords
    keywords = relationship("KeywordModel", secondary=docket_keywords, back_populates="dockets")

class KeywordModel(Base):
    """SQLAlchemy model for keywords."""
    __tablename__ = "keywords"

    id = Column(Integer, primary_key=True, autoincrement=True)
    text = Column(String, nullable=False, unique=True, index=True)
    
    # Relationship with dockets
    dockets = relationship("DocketModel", secondary=docket_keywords, back_populates="keywords")
