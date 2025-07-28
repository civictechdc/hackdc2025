"""
Database service for CRUD operations.
"""
from typing import List, Optional, Set
import json

from sqlalchemy.orm import Session

from src.backend.models.domain.docket import Docket
from src.backend.models.database.database_models import DocketModel, KeywordModel

class DocketService:
    """Service for database operations on dockets."""
    
    def __init__(self, db: Session):
        """Initialize the service with a database session.
        
        Args:
            db: SQLAlchemy database session.
        """
        self.db = db
    
    def get_docket(self, docket_id: int) -> Optional[Docket]:
        """Get a docket by ID.
        
        Args:
            docket_id: The docket ID.
            
        Returns:
            Optional[Docket]: The docket if found, None otherwise.
        """
        db_docket = self.db.query(DocketModel).filter(DocketModel.docket_id == docket_id).first()
        if not db_docket:
            return None
            
        return self._convert_to_domain(db_docket)
    
    def get_all_dockets(self, skip: int = 0, limit: int = 100) -> List[Docket]:
        """Get all dockets.
        
        Args:
            skip: Number of records to skip.
            limit: Maximum number of records to return.
            
        Returns:
            List[Docket]: List of dockets.
        """
        db_dockets = self.db.query(DocketModel).offset(skip).limit(limit).all()
        return [self._convert_to_domain(d) for d in db_dockets]
    
    def create_docket(self, docket: Docket) -> Docket:
        """Create a new docket.
        
        Args:
            docket: The docket data.
            
        Returns:
            Docket: The created docket.
        """
        db_docket = DocketModel(
            docket_id=docket.docket_id,
            title=docket.title,
            summary=docket.summary
        )
        
        self.db.add(db_docket)
        self.db.commit()
        self.db.refresh(db_docket)
        
        # Add keywords if provided
        if docket.keywords:
            self._add_keywords_to_docket(db_docket, docket.keywords)
        
        return self._convert_to_domain(db_docket)
    
    def update_docket(self, docket_id: int, title: str = None, 
                     summary: str = None, keywords: Set[str] = None) -> Optional[Docket]:
        """Update a docket.
        
        Args:
            docket_id: The docket ID.
            title: Optional new title.
            summary: Optional new summary.
            keywords: Optional new keywords.
            
        Returns:
            Optional[Docket]: The updated docket if found, None otherwise.
        """
        db_docket = self.db.query(DocketModel).filter(DocketModel.docket_id == docket_id).first()
        if not db_docket:
            return None
            
        if title is not None:
            db_docket.title = title
        if summary is not None:
            db_docket.summary = summary
        
        self.db.commit()
        
        if keywords is not None:
            self._add_keywords_to_docket(db_docket, keywords)
        
        return self._convert_to_domain(db_docket)
    
    def _get_or_create_keyword(self, text: str) -> KeywordModel:
        """Get or create a keyword.
        
        Args:
            text: The keyword text.
            
        Returns:
            KeywordModel: The keyword model.
        """
        keyword = self.db.query(KeywordModel).filter(KeywordModel.text == text).first()
        if not keyword:
            keyword = KeywordModel(text=text)
            self.db.add(keyword)
            self.db.commit()
            self.db.refresh(keyword)
        return keyword
    
    def _add_keywords_to_docket(self, db_docket: DocketModel, keywords: Set[str]) -> None:
        """Add keywords to a docket.
        
        Args:
            db_docket: The database docket model.
            keywords: Set of keywords to add.
        """
        # First clear existing keywords
        db_docket.keywords = []
        
        # Add new keywords
        for keyword_text in keywords:
            keyword = self._get_or_create_keyword(keyword_text)
            db_docket.keywords.append(keyword)
        
        self.db.commit()
        self.db.refresh(db_docket)
    
    def search_dockets_by_keyword(self, search_term: str) -> List[Docket]:
        """Search for dockets by keyword.
        
        Args:
            search_term: The search term.
            
        Returns:
            List[Docket]: List of matching dockets.
        """
        db_dockets = (
            self.db.query(DocketModel)
            .join(DocketModel.keywords)
            .filter(KeywordModel.text.ilike(f"%{search_term}%"))
            .distinct()
            .all()
        )
        
        return [self._convert_to_domain(d) for d in db_dockets]
    
    def _convert_to_domain(self, db_docket: DocketModel) -> Docket:
        """Convert a database model to a domain model.
        
        Args:
            db_docket: The database docket model.
            
        Returns:
            Docket: The domain docket model.
        """
        keywords = {keyword.text for keyword in db_docket.keywords}
        
        return Docket(
            docket_id=db_docket.docket_id,
            title=db_docket.title,
            summary=db_docket.summary,
            keywords=keywords
        )
    
    def load_dockets_from_json(self, json_path: str) -> int:
        """Load dockets from a JSON file.
        
        Args:
            json_path: Path to the JSON file.
            
        Returns:
            int: Number of dockets loaded.
        """
        with open(json_path, 'r', encoding='utf-8') as f:
            docket_data = json.load(f)
        
        count = 0
        for item in docket_data:
            # Check if docket already exists
            existing_docket = self.get_docket(item['docket_id'])
            if existing_docket:
                # Update existing docket
                self.update_docket(
                    docket_id=item['docket_id'],
                    title=item['title'],
                    summary=item['summary']
                )
            else:
                # Create new docket
                docket = Docket(
                    docket_id=item['docket_id'],
                    title=item['title'],
                    summary=item['summary']
                )
                self.create_docket(docket)
            
            count += 1
        
        return count
