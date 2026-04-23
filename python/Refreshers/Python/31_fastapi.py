"""
FASTAPI - MODERN ASYNC WEB FRAMEWORK
=====================================
FastAPI is a modern, fast web framework for building APIs with Python 3.7+
based on standard Python type hints.

Features:
- Fast: Very high performance, on par with NodeJS and Go
- Fast to code: Type hints for auto-completion and validation
- Fewer bugs: Reduce developer-induced errors
- Standards-based: OpenAPI, JSON Schema
- Automatic documentation: Interactive API docs (Swagger UI)
"""

print("=" * 80)
print("FASTAPI - MODERN ASYNC WEB FRAMEWORK")
print("=" * 80)

# ============================================================================
# 1. INSTALLATION AND BASIC SETUP
# ============================================================================

"""
INSTALLATION:
pip install fastapi
pip install "uvicorn[standard]"  # ASGI server

REQUIREMENTS:
- Python 3.7+
- Pydantic for data validation
- Starlette for web parts
"""

# ============================================================================
# 2. BASIC FASTAPI APPLICATION
# ============================================================================

from fastapi import FastAPI, HTTPException, Query, Path, Body, Header, Cookie
from fastapi import status, Depends, Request, Response
from fastapi.responses import JSONResponse, HTMLResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, Field, validator, EmailStr
from typing import Optional, List, Dict, Any
from datetime import datetime, timedelta
from enum import Enum
import uvicorn

# Create FastAPI instance
app = FastAPI(
    title="My API",
    description="API built with FastAPI",
    version="1.0.0",
    docs_url="/docs",  # Swagger UI
    redoc_url="/redoc"  # ReDoc
)

# Basic route
@app.get("/")
async def root():
    """Root endpoint - returns welcome message"""
    return {"message": "Welcome to FastAPI!"}

# Route with path parameter
@app.get("/items/{item_id}")
async def read_item(item_id: int):
    """
    Read an item by ID
    
    Path parameters are automatically validated and converted
    """
    return {"item_id": item_id, "name": f"Item {item_id}"}


# ============================================================================
# 3. PYDANTIC MODELS FOR REQUEST/RESPONSE
# ============================================================================

"""
PYDANTIC MODELS:
- Define data structures with type hints
- Automatic validation
- Automatic documentation
- JSON serialization/deserialization
"""

class UserBase(BaseModel):
    """Base user model"""
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    full_name: Optional[str] = None
    
class UserCreate(UserBase):
    """Model for creating users"""
    password: str = Field(..., min_length=8)
    
class UserResponse(UserBase):
    """Model for user responses (no password)"""
    id: int
    created_at: datetime
    is_active: bool = True
    
    class Config:
        orm_mode = True  # Allow creating from ORM objects

class ItemBase(BaseModel):
    """Base item model"""
    name: str
    description: Optional[str] = None
    price: float = Field(..., gt=0, description="Price must be positive")
    tax: Optional[float] = None
    tags: List[str] = []
    
    @validator('price')
    def price_must_be_positive(cls, v):
        """Custom validator"""
        if v <= 0:
            raise ValueError('Price must be positive')
        return v

class ItemCreate(ItemBase):
    """Model for creating items"""
    pass

class ItemResponse(ItemBase):
    """Model for item responses"""
    id: int
    owner_id: int
    created_at: datetime
    
    class Config:
        orm_mode = True


# ============================================================================
# 4. REQUEST BODY AND VALIDATION
# ============================================================================

@app.post("/users/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate):
    """
    Create a new user
    
    - **username**: unique username (3-50 chars)
    - **email**: valid email address
    - **password**: password (min 8 chars)
    - **full_name**: optional full name
    """
    # In real app: hash password, save to database
    user_dict = user.dict()
    user_dict["id"] = 1
    user_dict["created_at"] = datetime.now()
    user_dict["is_active"] = True
    return UserResponse(**user_dict)

@app.post("/items/", response_model=ItemResponse)
async def create_item(item: ItemCreate):
    """Create a new item with automatic validation"""
    item_dict = item.dict()
    item_dict["id"] = 1
    item_dict["owner_id"] = 1
    item_dict["created_at"] = datetime.now()
    return ItemResponse(**item_dict)


# ============================================================================
# 5. QUERY PARAMETERS
# ============================================================================

@app.get("/items/")
async def list_items(
    skip: int = Query(0, ge=0, description="Number of items to skip"),
    limit: int = Query(10, ge=1, le=100, description="Number of items to return"),
    q: Optional[str] = Query(None, min_length=3, description="Search query")
):
    """
    List items with pagination and search
    
    Query parameters:
    - skip: offset (default 0)
    - limit: page size (default 10, max 100)
    - q: search query (optional, min 3 chars)
    """
    items = [{"id": i, "name": f"Item {i}"} for i in range(skip, skip + limit)]
    return {
        "items": items,
        "skip": skip,
        "limit": limit,
        "query": q
    }


# ============================================================================
# 6. PATH PARAMETERS WITH VALIDATION
# ============================================================================

@app.get("/users/{user_id}/items/{item_id}")
async def read_user_item(
    user_id: int = Path(..., gt=0, description="User ID"),
    item_id: int = Path(..., gt=0, description="Item ID")
):
    """
    Get specific item for specific user
    
    Path parameters with validation:
    - user_id: must be > 0
    - item_id: must be > 0
    """
    return {"user_id": user_id, "item_id": item_id}


# ============================================================================
# 7. REQUEST HEADERS AND COOKIES
# ============================================================================

@app.get("/headers/")
async def read_headers(
    user_agent: Optional[str] = Header(None),
    accept_language: Optional[str] = Header(None),
    x_custom_header: Optional[str] = Header(None)
):
    """Read request headers"""
    return {
        "User-Agent": user_agent,
        "Accept-Language": accept_language,
        "X-Custom-Header": x_custom_header
    }

@app.get("/cookies/")
async def read_cookies(
    session_id: Optional[str] = Cookie(None)
):
    """Read cookies"""
    return {"session_id": session_id}


# ============================================================================
# 8. RESPONSE MODELS AND STATUS CODES
# ============================================================================

class ErrorResponse(BaseModel):
    """Standard error response"""
    detail: str
    code: Optional[str] = None

@app.get(
    "/items/{item_id}",
    response_model=ItemResponse,
    responses={
        200: {"description": "Item found"},
        404: {"model": ErrorResponse, "description": "Item not found"}
    }
)
async def get_item(item_id: int):
    """Get item by ID with proper response models"""
    if item_id > 100:
        raise HTTPException(
            status_code=404,
            detail="Item not found",
            headers={"X-Error": "Item-Not-Found"}
        )
    
    return {
        "id": item_id,
        "name": f"Item {item_id}",
        "description": "A sample item",
        "price": 29.99,
        "tax": 2.99,
        "tags": ["sample"],
        "owner_id": 1,
        "created_at": datetime.now()
    }


# ============================================================================
# 9. DEPENDENCY INJECTION
# ============================================================================

"""
DEPENDENCY INJECTION:
- Reusable logic
- Shared database connections
- Authentication
- Validation
"""

# Simple dependency
def get_current_user(token: str = Header(..., alias="Authorization")):
    """
    Dependency: Extract and validate user from token
    Can be reused across multiple endpoints
    """
    if not token.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid token format")
    
    # In real app: validate JWT token
    return {"user_id": 1, "username": "alice"}

# Database dependency (example)
class DatabaseSession:
    """Simulated database session"""
    def __init__(self):
        self.is_active = True
    
    def close(self):
        self.is_active = False

def get_db():
    """
    Dependency: Database session with cleanup
    """
    db = DatabaseSession()
    try:
        yield db
    finally:
        db.close()

# Use dependencies
@app.get("/users/me")
async def read_users_me(current_user: dict = Depends(get_current_user)):
    """
    Get current user info
    Requires authentication via Depends
    """
    return current_user

@app.get("/protected/")
async def protected_route(
    current_user: dict = Depends(get_current_user),
    db: DatabaseSession = Depends(get_db)
):
    """Protected route with multiple dependencies"""
    return {
        "user": current_user,
        "db_active": db.is_active
    }


# ============================================================================
# 10. BACKGROUND TASKS
# ============================================================================

from fastapi import BackgroundTasks

def send_email(email: str, message: str):
    """
    Simulated email sending (runs in background)
    """
    import time
    time.sleep(2)  # Simulate slow operation
    print(f"Sending email to {email}: {message}")

@app.post("/send-notification/")
async def send_notification(
    email: str,
    background_tasks: BackgroundTasks
):
    """
    Send notification in background
    Response returned immediately, task runs after
    """
    background_tasks.add_task(send_email, email, "Notification message")
    return {"message": "Notification will be sent"}


# ============================================================================
# 11. MIDDLEWARE
# ============================================================================

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production: specify allowed origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Custom middleware
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    """
    Custom middleware: Add processing time header
    """
    import time
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response


# ============================================================================
# 12. FILE UPLOADS
# ============================================================================

from fastapi import File, UploadFile

@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    """
    Upload a file
    
    UploadFile provides:
    - filename
    - content_type
    - file (SpooledTemporaryFile)
    """
    contents = await file.read()
    return {
        "filename": file.filename,
        "content_type": file.content_type,
        "size": len(contents)
    }

@app.post("/uploadfiles/")
async def upload_multiple_files(files: List[UploadFile] = File(...)):
    """Upload multiple files"""
    return [
        {
            "filename": file.filename,
            "content_type": file.content_type
        }
        for file in files
    ]


# ============================================================================
# 13. WEBSOCKETS
# ============================================================================

from fastapi import WebSocket, WebSocketDisconnect

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """
    WebSocket endpoint for real-time communication
    """
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            await websocket.send_text(f"Message received: {data}")
    except WebSocketDisconnect:
        print("Client disconnected")


# ============================================================================
# 14. DATABASE INTEGRATION (SQLAlchemy Example)
# ============================================================================

"""
DATABASE WITH SQLALCHEMY:

from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

class UserDB(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)

Base.metadata.create_all(bind=engine)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Usage in route
@app.post("/users/", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = UserDB(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
"""


# ============================================================================
# 15. AUTHENTICATION (JWT Example)
# ============================================================================

"""
JWT AUTHENTICATION:

from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import timedelta

SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain, hashed):
    return pwd_context.verify(plain, hashed)

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

@app.post("/token")
async def login(username: str, password: str):
    # Verify credentials (check database)
    # ...
    access_token = create_access_token(data={"sub": username})
    return {"access_token": access_token, "token_type": "bearer"}
"""


# ============================================================================
# 16. TESTING FASTAPI
# ============================================================================

"""
TESTING WITH TESTCLIENT:

from fastapi.testclient import TestClient

client = TestClient(app)

def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to FastAPI!"}

def test_create_user():
    response = client.post(
        "/users/",
        json={
            "username": "testuser",
            "email": "test@example.com",
            "password": "password123"
        }
    )
    assert response.status_code == 201
    assert response.json()["username"] == "testuser"
"""


# ============================================================================
# 17. BEST PRACTICES
# ============================================================================

"""
FASTAPI BEST PRACTICES:

1. PROJECT STRUCTURE:
   app/
   ├── main.py              # FastAPI app
   ├── models.py            # Pydantic models
   ├── database.py          # Database setup
   ├── crud.py              # CRUD operations
   ├── dependencies.py      # Dependency functions
   ├── routers/             # API routers
   │   ├── users.py
   │   └── items.py
   └── tests/               # Tests

2. ROUTER ORGANIZATION:
   - Split routes into separate files
   - Use APIRouter for modularization
   - Include routers in main app

3. DEPENDENCIES:
   - Reuse common logic
   - Database sessions
   - Authentication
   - Rate limiting

4. VALIDATION:
   - Use Pydantic models
   - Custom validators
   - Response models

5. DOCUMENTATION:
   - Add docstrings to endpoints
   - Use response_model
   - Document error responses
   - Add examples

6. SECURITY:
   - Use HTTPS in production
   - Implement proper authentication
   - Rate limiting
   - CORS configuration
   - Input validation

7. PERFORMANCE:
   - Use async/await properly
   - Connection pooling
   - Caching (Redis)
   - Background tasks for slow operations

8. ERROR HANDLING:
   - Use HTTPException
   - Custom exception handlers
   - Proper status codes
   - Error logging

9. TESTING:
   - TestClient for API testing
   - pytest for test framework
   - Mock dependencies
   - Test coverage

10. DEPLOYMENT:
    - Use production ASGI server (Gunicorn + Uvicorn)
    - Environment variables
    - Docker containerization
    - Health check endpoint
"""


# ============================================================================
# RUNNING THE APPLICATION
# ============================================================================

if __name__ == "__main__":
    # Development server
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True  # Auto-reload on code changes
    )

"""
RUNNING:

Development:
uvicorn main:app --reload

Production (with Gunicorn):
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker

AUTOMATIC DOCUMENTATION:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
- OpenAPI JSON: http://localhost:8000/openapi.json

KEY TAKEAWAYS:

1. FastAPI uses type hints for validation and documentation
2. Pydantic models for request/response validation
3. Automatic interactive API documentation
4. Dependency injection for reusable logic
5. Async/await for high performance
6. Easy testing with TestClient
7. Built-in security utilities
8. WebSocket support
9. Background tasks
10. Production-ready with proper structure
"""

print("\n=== FastAPI Complete ===")
