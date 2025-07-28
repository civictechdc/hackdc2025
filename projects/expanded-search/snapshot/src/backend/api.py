"""API module for serving the frontend with data."""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Dict, Any

from src.backend.database.db_manager import get_all_dockets, search_dockets
from src.backend.models.domain.docket import Docket

# TODO: move routes to a different folder/file

# Create FastAPI instance
app = FastAPI(
    title="Regulations API",
    description="API for retrieving and searching regulation dockets",
    version="1.0.0"
)

# Add CORS middleware to allow requests from the Angular frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],  # Angular dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Helper function to convert Docket objects to dictionaries
def docket_to_dict(docket: Docket) -> Dict[str, Any]:
    """Convert a Docket object to a dictionary for JSON response."""
    return {
        "docket_id": docket.docket_id,
        "title": docket.title,
        "summary": docket.summary,
        "keywords": list(docket.keywords) if docket.keywords else []
    }

@app.get("/")
def read_root():
    """Root endpoint that shows API is running."""
    return {"message": "Regulations API is running"}

@app.get("/api/regulations", response_model=List[Dict[str, Any]])
def get_regulations():
    """Get all regulations."""
    dockets = get_all_dockets()
    return [docket_to_dict(docket) for docket in dockets]


# TODO: change /search/ to /keyword-search/
@app.get("/api/regulations/search/{search_term}", response_model=List[Dict[str, Any]])
def search_regulations(search_term: str):
    """Search for regulations by keyword."""
    if not search_term or len(search_term.strip()) < 2:
        raise HTTPException(status_code=400, detail="Search term must be at least 2 characters")
    
    dockets = search_dockets(search_term)
    return [docket_to_dict(docket) for docket in dockets]

@app.get("/api/regulations/{docket_id}", response_model=Dict[str, Any])
def get_regulation(docket_id: int):
    """Get a regulation by ID."""
    dockets = get_all_dockets()
    for docket in dockets:
        if docket.docket_id == docket_id:
            return docket_to_dict(docket)
    
    raise HTTPException(status_code=404, detail="Regulation not found")
