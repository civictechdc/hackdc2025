"""Database management utilities."""
from contextlib import contextmanager
from typing import List, Generator

from sqlalchemy.orm import Session

from src.backend.database.database import get_db, create_db_and_tables
from src.backend.database.docket_service import DocketService
from src.backend.models.domain.docket import Docket
from src.backend.keywords.local_nlp_keyword_service import LocalNLPKeywordService

@contextmanager
def get_db_session() -> Generator[Session, None, None]:
    """Context manager for database sessions.
    
    Yields:
        Session: A database session.
    """
    db = next(get_db())
    try:
        yield db
    finally:
        db.close()

def initialize_database() -> None:
    """Initialize the database by creating tables."""
    create_db_and_tables()

def process_dockets_with_keywords(json_path: str) -> int:
    """Process dockets from JSON, extract keywords, and save to database.
    
    Args:
        json_path: Path to the JSON file containing docket data.
        
    Returns:
        int: Number of dockets processed.
    """
    # Initialize database
    initialize_database()
    
    # Load dockets from JSON
    with get_db_session() as db:
        docket_service = DocketService(db)
        count = docket_service.load_dockets_from_json(json_path)
    
    # Extract and save keywords
    with get_db_session() as db:
        docket_service = DocketService(db)
        
        # Get all dockets as domain models
        dockets = docket_service.get_all_dockets()
        
        # Extract keywords
        keyword_service = LocalNLPKeywordService()
        keyword_service.extract_keywords(dockets)
        
        # Save keywords back to database
        for docket in dockets:
            if docket.keywords:
                docket_service.update_docket(
                    docket_id=docket.docket_id,
                    keywords=docket.keywords
                )

    print(f"Processed dockets and extracted keywords: {dockets}")

    return count

def get_all_dockets() -> List[Docket]:
    """Get all dockets from the database.
    
    Returns:
        List[Docket]: List of dockets as domain models.
    """
    with get_db_session() as db:
        docket_service = DocketService(db)
        return docket_service.get_all_dockets()

def search_dockets(search_term: str) -> List[Docket]:
    """Search for dockets by keyword.
    
    Args:
        search_term: Term to search for.
        
    Returns:
        List[Docket]: List of matching dockets.
    """
    with get_db_session() as db:
        docket_service = DocketService(db)
        # For now, we just want to return the dockets that have the keyword matching the search term
        return docket_service.search_dockets_by_keyword(search_term)
