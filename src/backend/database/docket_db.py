"""Database module for storing and retrieving docket data."""
import os
import sqlite3
import json
from pathlib import Path
from typing import List, Optional, Dict, Any

from src.backend.models.domain.docket import Docket

class DocketDatabase:
    """Handles database operations for dockets."""
    
    def __init__(self, db_path: Optional[str] = None):
        """Initialize the database connection."""
        if db_path is None:
            # Use default path in project directory
            project_root = Path(__file__).parent.parent.parent.parent
            db_path = os.path.join(project_root, 'regulations.db')
        
        self.db_path = db_path
        self._initialize_db()
    
    def _initialize_db(self) -> None:
        """Create the database and tables if they don't exist."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create tables
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS dockets (
            docket_id INTEGER PRIMARY KEY,
            title TEXT NOT NULL,
            summary TEXT NOT NULL,
            last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS keywords (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            docket_id INTEGER,
            keyword TEXT NOT NULL,
            FOREIGN KEY (docket_id) REFERENCES dockets (docket_id),
            UNIQUE(docket_id, keyword)
        )
        ''')
        
        conn.commit()
        conn.close()
    
    def save_docket(self, docket: Docket) -> None:
        """Save a docket to the database."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Insert or replace the docket
        cursor.execute('''
        INSERT OR REPLACE INTO dockets (docket_id, title, summary) 
        VALUES (?, ?, ?)
        ''', (docket.docket_id, docket.title, docket.summary))
        
        # Delete existing keywords for this docket
        cursor.execute('DELETE FROM keywords WHERE docket_id = ?', (docket.docket_id,))
        
        # Insert new keywords
        if docket.keywords:
            keyword_values = [(docket.docket_id, keyword) for keyword in docket.keywords]
            cursor.executemany(
                'INSERT INTO keywords (docket_id, keyword) VALUES (?, ?)',
                keyword_values
            )
        
        conn.commit()
        conn.close()
    
    def save_dockets(self, dockets: List[Docket]) -> None:
        """Save multiple dockets to the database."""
        for docket in dockets:
            self.save_docket(docket)
    
    def get_docket(self, docket_id: int) -> Optional[Docket]:
        """Retrieve a docket by ID."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Get the docket
        cursor.execute('SELECT docket_id, title, summary FROM dockets WHERE docket_id = ?', (docket_id,))
        docket_row = cursor.fetchone()
        
        if not docket_row:
            conn.close()
            return None
        
        # Get the keywords
        cursor.execute('SELECT keyword FROM keywords WHERE docket_id = ?', (docket_id,))
        keywords = [row[0] for row in cursor.fetchall()]
        
        conn.close()
        
        return Docket(
            docket_id=docket_row[0],
            title=docket_row[1],
            summary=docket_row[2],
            keywords=set(keywords) if keywords else None
        )
    
    def get_all_dockets(self) -> List[Docket]:
        """Retrieve all dockets."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Get all dockets
        cursor.execute('SELECT docket_id, title, summary FROM dockets')
        docket_rows = cursor.fetchall()
        
        dockets = []
        for docket_row in docket_rows:
            docket_id = docket_row[0]
            
            # Get keywords for this docket
            cursor.execute('SELECT keyword FROM keywords WHERE docket_id = ?', (docket_id,))
            keywords = [row[0] for row in cursor.fetchall()]
            
            dockets.append(Docket(
                docket_id=docket_id,
                title=docket_row[1],
                summary=docket_row[2],
                keywords=set(keywords) if keywords else None
            ))
        
        conn.close()
        return dockets
    
    def search_dockets(self, search_term: str) -> List[Docket]:
        """Search for dockets by keyword."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        # Search for dockets that have a matching keyword
        cursor.execute('''
        SELECT d.docket_id, d.title, d.summary
        FROM dockets d
        JOIN keywords k ON d.docket_id = k.docket_id
        WHERE LOWER(k.keyword) LIKE LOWER(?)
        GROUP BY d.docket_id
        ''', (f'%{search_term}%',))
        
        docket_rows = cursor.fetchall()
        dockets = []
        
        for docket_row in docket_rows:
            docket_id = docket_row['docket_id']
            
            # Get keywords for this docket
            cursor.execute('SELECT keyword FROM keywords WHERE docket_id = ?', (docket_id,))
            keywords = [row[0] for row in cursor.fetchall()]
            
            dockets.append(Docket(
                docket_id=docket_id,
                title=docket_row['title'],
                summary=docket_row['summary'],
                keywords=set(keywords) if keywords else None
            ))
        
        conn.close()
        return dockets
    
    def update_from_json(self, json_path: str) -> int:
        """Update the database from a JSON file containing dockets data.
        
        Returns:
            int: Number of dockets updated
        """
        with open(json_path, 'r', encoding='utf-8') as f:
            docket_data = json.load(f)
        
        dockets = [Docket(**item) for item in docket_data]
        self.save_dockets(dockets)
        return len(dockets)
