from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from sqlalchemy import create_engine, Column, Integer, String, Boolean, ForeignKey, Text, DateTime, BigInteger
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session, relationship
from datetime import datetime
import os

# --- Database Setup ---
# Updated to use 'postgres' as host
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@postgres:5432/carserv")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# --- Models ---

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    role = Column(String(50), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    # Simplified relationships/FK for demo purposes
    # modified_by...

class Page(Base):
    __tablename__ = "pages"
    id = Column(BigInteger, primary_key=True, index=True)
    name = Column(String(150), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    added_by = Column(BigInteger, ForeignKey("users.id"))

class ContentItem(Base):
    __tablename__ = "content_items"
    id = Column(BigInteger, primary_key=True, index=True)
    page_id = Column(BigInteger, ForeignKey("pages.id"))
    position = Column(Integer, nullable=False)
    title = Column(String(255))
    content = Column(Text)
    content_type = Column(String(50), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

# --- Dependency ---
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- Auth ---
security = HTTPBasic()

def get_current_username(credentials: HTTPBasicCredentials = Depends(security)):
    # Simple auth for demo
    if credentials.username != "admin" or credentials.password != "admin":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username

# --- App ---
app = FastAPI(title="CarServ CMS API")

@app.get("/")
def read_root():
    return {"message": "Welcome to CarServ CMS API. Visit /docs for Swagger UI."}

# Endpoint 1: Users (Updated)
@app.get("/users", dependencies=[Depends(get_current_username)])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = db.query(User).offset(skip).limit(limit).all()
    return users

# Endpoint 2: Pages (New)
@app.get("/pages", dependencies=[Depends(get_current_username)])
def read_pages(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    pages = db.query(Page).offset(skip).limit(limit).all()
    return pages

# Endpoint 3: Content Items (New)
@app.get("/content", dependencies=[Depends(get_current_username)])
def read_content(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    content = db.query(ContentItem).offset(skip).limit(limit).all()
    return content