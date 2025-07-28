# Regulations Commenting System

A system for extracting, storing, and searching regulation dockets using NLP keyword extraction.

## Architecture

This application consists of:

1. **Python Backend**
   - SQLAlchemy ORM for database operations
   - spaCy for NLP keyword extraction
   - SQLite database for storing dockets and keywords
   - Domain models for business logic

2. **Angular Frontend**
   - Angular Material UI components
   - Search interface for regulations by keyword

## Setup

### 1. Install Python Dependencies
```
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

### 2. Database Setup
The application uses SQLAlchemy with SQLite for data storage. To initialize the database:

```
# Create initial migration
alembic revision --autogenerate -m "Initial migration"

# Apply migration
alembic upgrade head
```

### 3. Frontend Setup
Navigate to the Angular project directory and install dependencies:

```
cd src/frontend/regulations-search
npm install
```

## Running the Application

The application can be run in several ways:

### 1. Run Full Application (Backend + Frontend)

With database update (recommended for first run):
```
python main.py --update-db
```

Without database update (faster startup for subsequent runs):
```
python main.py
```

### 2. Run Backend Only

To only update the database and run the backend:
```
python main.py --update-db --backend-only
```

### 3. Run Frontend Only

To start only the Angular frontend:
```
python main.py --frontend-only
```

### 4. View the database contents

To view the database contents in a web browser:
```
python view_database.py --web
```

### 5. View and test the API

To view the API documentation and test the endpoints interactively:
```
python view_api.py
```

This will start the FastAPI server and open the Swagger UI in your web browser, where you can explore and test all available API endpoints.

## Technical Details

- The SQLite database file (regulations.db) is created in your project root directory and persists between runs.
- Keywords are extracted from docket titles and summaries using spaCy NLP.
- The frontend communicates with the backend via REST API endpoints.
- Database migrations are handled by Alembic.