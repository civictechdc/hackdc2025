"""Backend module for processing and serving regulation data."""
import os
from pathlib import Path
from typing import List

from src.backend.database.db_manager import process_dockets_with_keywords, get_all_dockets, search_dockets
from src.backend.models.domain.docket import Docket

def get_default_json_path() -> str:
    """Get the default JSON path for dockets data.
    
    Returns:
        str: Path to the default dockets JSON file.
    """
    project_root = Path(__file__).parent.parent.parent
    return os.path.join(project_root, 'temp-data', 'dockets.json')

def update_dockets_data(json_path: str = None) -> int:
    """Process dockets from the JSON file and update the database.
    
    Args:
        json_path: Optional path to the JSON file. If not provided, uses default.
        
    Returns:
        int: Number of dockets processed.
    """
    if json_path is None:
        json_path = get_default_json_path()
    
    # Check if file exists before processing
    if os.path.exists(json_path):
        return process_dockets_with_keywords(json_path)
    else:
        print(f"Error: JSON file not found at {json_path}")
        return 0

def get_regulations() -> List[Docket]:
    """Get all regulations from the database.
    
    Returns:
        List[Docket]: List of all dockets.
    """
    return get_all_dockets()

def search_regulations(search_term: str) -> List[Docket]:
    """Search for regulations by keyword.
    
    Args:
        search_term: Term to search for.
        
    Returns:
        List[Docket]: List of matching dockets.
    """
    return search_dockets(search_term)

def run(update_data: bool = True) -> None:
    """Run the backend, processing data and starting any necessary services.
    
    Args:
        update_data: Whether to update the database with the latest data.
    """
    if update_data:
        num_dockets = update_dockets_data()
        print(f"Processed {num_dockets} dockets")
    
    # Here you would start any API servers or services
    # For now, just print some information
    dockets = get_regulations()

    print(f"Database contains {len(dockets)} dockets")
    
    # Start the FastAPI server using Uvicorn
    import uvicorn
    import threading
    import signal
    import sys
    from src.backend.api import app
    
    print("Starting FastAPI server...")
    
    # Use a Server instance instead of the simple run method
    # This allows for graceful shutdown
    server = uvicorn.Server(
        config=uvicorn.Config(
            app=app,
            host="0.0.0.0",
            port=8000,
            log_level="info"
        )
    )
    
    # Run server in the current thread
    try:
        server.run()
    except KeyboardInterrupt:
        print("Shutting down server...")
        sys.exit(0)
