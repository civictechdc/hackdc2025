"""
CRUD operations for the database.

DEPRECATED: This module is being phased out in favor of the DocketService class.
Please use src.backend.database.docket_service.DocketService for all database operations.
"""
import json
from typing import List, Optional, Set

from sqlalchemy.orm import Session

from src.backend.models.database.database_models import DocketModel, KeywordModel
from src.backend.models.pydantic_models import Docket, DocketCreate

def get_docket(db: Session, docket_id: int) -> Optional[DocketModel]:
    """Get a docket by ID.
    
    Args:
        db: Database session.
        docket_id: The docket ID.
        
    Returns:
        Optional[DocketModel]: The docket model if found, None otherwise.
    """
    return db.query(DocketModel).filter(DocketModel.docket_id == docket_id).first()

def get_all_dockets(db: Session, skip: int = 0, limit: int = 100) -> List[DocketModel]:
    """Get all dockets.
    
    Args:
        db: Database session.
        skip: Number of records to skip.
        limit: Maximum number of records to return.
        
    Returns:
        List[DocketModel]: List of docket models.
    """
    return db.query(DocketModel).offset(skip).limit(limit).all()

def get_or_create_keyword(db: Session, text: str) -> KeywordModel:
    """Get or create a keyword.
    
    Args:
        db: Database session.
        text: The keyword text.
        
    Returns:
        KeywordModel: The keyword model.
    """
    keyword = db.query(KeywordModel).filter(KeywordModel.text == text).first()
    if not keyword:
        keyword = KeywordModel(text=text)
        db.add(keyword)
        db.commit()
        db.refresh(keyword)
    return keyword

def create_docket(db: Session, docket: DocketCreate, keywords: Set[str] = None) -> DocketModel:
    """Create a new docket.
    
    Args:
        db: Database session.
        docket: The docket data.
        keywords: Optional set of keywords.
        
    Returns:
        DocketModel: The created docket model.
    """
    db_docket = DocketModel(
        docket_id=docket.docket_id,
        title=docket.title,
        summary=docket.summary
    )
    
    db.add(db_docket)
    db.commit()
    db.refresh(db_docket)
    
    # Add keywords if provided
    if keywords:
        add_keywords_to_docket(db, db_docket, keywords)
    
    return db_docket

def update_docket(db: Session, docket_model: DocketModel, 
                 title: str = None, summary: str = None) -> DocketModel:
    """Update a docket.
    
    Args:
        db: Database session.
        docket_model: The docket model to update.
        title: Optional new title.
        summary: Optional new summary.
        
    Returns:
        DocketModel: The updated docket model.
    """
    if title is not None:
        docket_model.title = title
    if summary is not None:
        docket_model.summary = summary
    
    db.commit()
    db.refresh(docket_model)
    
    return docket_model

def add_keywords_to_docket(db: Session, docket_model: DocketModel, keywords: Set[str]) -> DocketModel:
    """Add keywords to a docket.
    
    Args:
        db: Database session.
        docket_model: The docket model.
        keywords: Set of keywords to add.
        
    Returns:
        DocketModel: The updated docket model.
    """
    # First clear existing keywords
    docket_model.keywords = []
    
    # Add new keywords
    for keyword_text in keywords:
        keyword = get_or_create_keyword(db, keyword_text)
        docket_model.keywords.append(keyword)
    
    db.commit()
    db.refresh(docket_model)
    
    return docket_model

def search_dockets_by_keyword(db: Session, search_term: str) -> List[DocketModel]:
    """Search for dockets by keyword.
    
    Args:
        db: Database session.
        search_term: The search term.
        
    Returns:
        List[DocketModel]: List of matching docket models.
    """
    return (
        db.query(DocketModel)
        .join(DocketModel.keywords)
        .filter(KeywordModel.text.ilike(f"%{search_term}%"))
        .distinct()
        .all()
    )

def convert_to_pydantic(docket_model: DocketModel) -> Docket:
    """Convert a SQLAlchemy model to a Pydantic model.
    
    Args:
        docket_model: The SQLAlchemy docket model.
        
    Returns:
        Docket: The Pydantic docket model.
    """
    keywords = {keyword.text for keyword in docket_model.keywords}
    
    return Docket(
        docket_id=docket_model.docket_id,
        title=docket_model.title,
        summary=docket_model.summary,
        keywords=keywords
    )

def load_dockets_from_json(db: Session, json_path: str) -> int:
    """Load dockets from a JSON file.
    
    Args:
        db: Database session.
        json_path: Path to the JSON file.
        
    Returns:
        int: Number of dockets loaded.
    """
    with open(json_path, 'r', encoding='utf-8') as f:
        docket_data = json.load(f)
    
    count = 0
    for item in docket_data:
        docket = DocketCreate(
            docket_id=item['docket_id'],
            title=item['title'],
            summary=item['summary']
        )
        
        # Check if docket already exists
        existing_docket = get_docket(db, docket.docket_id)
        if existing_docket:
            # Update existing docket
            update_docket(db, existing_docket, title=docket.title, summary=docket.summary)
        else:
            # Create new docket
            create_docket(db, docket)
        
        count += 1
    
    return count
