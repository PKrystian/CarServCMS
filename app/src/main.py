from fastapi import FastAPI, Depends, HTTPException, status, Request, Form
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy import create_engine, Column, Integer, String, Boolean, ForeignKey, Text, DateTime, BigInteger
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session, relationship
from datetime import datetime
import bcrypt
from typing import Optional, List
from pydantic import BaseModel
import os

# --- Database Setup ---
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
    modified_by = Column(BigInteger)
    modified_at = Column(DateTime)

class Setting(Base):
    __tablename__ = "settings"
    id = Column(BigInteger, primary_key=True, index=True)
    reference_key = Column(String(255), nullable=False)
    value = Column(Text, nullable=False)
    added_by = Column(BigInteger, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    modified_by = Column(BigInteger, ForeignKey("users.id"))
    modified_at = Column(DateTime)

class Page(Base):
    __tablename__ = "pages"
    id = Column(BigInteger, primary_key=True, index=True)
    name = Column(String(150), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    added_by = Column(BigInteger, ForeignKey("users.id"))
    modified_by = Column(BigInteger, ForeignKey("users.id"))
    modified_at = Column(DateTime)

class ContentItem(Base):
    __tablename__ = "content_items"
    id = Column(BigInteger, primary_key=True, index=True)
    page_id = Column(BigInteger, ForeignKey("pages.id"))
    position = Column(Integer, nullable=False)
    title = Column(String(255))
    content = Column(Text)
    content_type = Column(String(50), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    added_by = Column(BigInteger, ForeignKey("users.id"))
    modified_by = Column(BigInteger, ForeignKey("users.id"))
    modified_at = Column(DateTime)

class Translation(Base):
    __tablename__ = "translations"
    id = Column(BigInteger, primary_key=True, index=True)
    reference_key = Column(String(255), nullable=False)
    language = Column(String(10), nullable=False)
    text = Column(Text)
    added_by = Column(BigInteger, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    modified_by = Column(BigInteger, ForeignKey("users.id"))
    modified_at = Column(DateTime)

# --- Pydantic Models ---

class PageCreate(BaseModel):
    name: str

class PageUpdate(BaseModel):
    name: Optional[str] = None

class ContentItemCreate(BaseModel):
    page_id: int
    position: int
    title: Optional[str] = None
    content: Optional[str] = None
    content_type: str

class ContentItemUpdate(BaseModel):
    position: Optional[int] = None
    title: Optional[str] = None
    content: Optional[str] = None
    content_type: Optional[str] = None

class SettingCreate(BaseModel):
    reference_key: str
    value: str

class SettingUpdate(BaseModel):
    value: Optional[str] = None

# --- Dependency ---
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- Auth ---
security = HTTPBasic()

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its bcrypt hash"""
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

def get_current_user(credentials: HTTPBasicCredentials = Depends(security), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == credentials.username).first()
    if not user or not verify_password(credentials.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return user

def get_admin_user(current_user: User = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
    return current_user

# --- App ---
app = FastAPI(title="CarServ CMS API")

# Mount static files
app.mount("/static", StaticFiles(directory="src/front"), name="static")

# Templates
templates = Jinja2Templates(directory="src/templates")

# --- Helper Functions ---

def get_settings_dict(db: Session):
    """Get all settings as a dictionary"""
    settings = db.query(Setting).all()
    return {s.reference_key: s.value for s in settings}

def get_page_content(db: Session, page_name: str):
    """Get page and its content items"""
    page = db.query(Page).filter(Page.name == page_name).first()
    if not page:
        return None, []
    content_items = db.query(ContentItem).filter(
        ContentItem.page_id == page.id
    ).order_by(ContentItem.position).all()
    return page, content_items

# --- Public Routes (Frontend) ---

@app.get("/", response_class=HTMLResponse)
async def home(request: Request, db: Session = Depends(get_db)):
    settings = get_settings_dict(db)
    page, content_items = get_page_content(db, "Home")

    # Organize content by type
    content = {
        'carousel': [],
        'features': [],
        'about': {},
        'about_points': [],
        'services': [],
        'booking_info': {}
    }

    for item in content_items:
        if item.content_type == 'carousel':
            content['carousel'].append(item)
        elif item.content_type == 'feature':
            content['features'].append(item)
        elif item.content_type == 'about':
            content['about'] = item
        elif item.content_type == 'about_point':
            content['about_points'].append(item)
        elif item.content_type == 'booking_info':
            content['booking_info'] = item

    return templates.TemplateResponse("index.html", {
        "request": request,
        "settings": settings,
        "page": page,
        "content": content
    })

@app.get("/about", response_class=HTMLResponse)
async def about(request: Request, db: Session = Depends(get_db)):
    settings = get_settings_dict(db)
    page, content_items = get_page_content(db, "About")

    content = {
        'header': {},
        'about': {},
        'about_points': []
    }

    for item in content_items:
        if item.content_type == 'page_header':
            content['header'] = item
        elif item.content_type == 'about':
            content['about'] = item
        elif item.content_type == 'about_point':
            content['about_points'].append(item)

    return templates.TemplateResponse("about.html", {
        "request": request,
        "settings": settings,
        "page": page,
        "content": content
    })

@app.get("/services", response_class=HTMLResponse)
async def services(request: Request, db: Session = Depends(get_db)):
    settings = get_settings_dict(db)
    page, content_items = get_page_content(db, "Services")

    content = {
        'header': {},
        'services': []
    }

    for item in content_items:
        if item.content_type == 'page_header':
            content['header'] = item
        elif item.content_type == 'service':
            content['services'].append(item)

    return templates.TemplateResponse("services.html", {
        "request": request,
        "settings": settings,
        "page": page,
        "content": content
    })

@app.get("/contact", response_class=HTMLResponse)
async def contact(request: Request, db: Session = Depends(get_db)):
    settings = get_settings_dict(db)
    page, content_items = get_page_content(db, "Contact")

    content = {
        'header': {},
        'intro': {}
    }

    for item in content_items:
        if item.content_type == 'page_header':
            content['header'] = item
        elif item.content_type == 'contact_intro':
            content['intro'] = item

    return templates.TemplateResponse("contact.html", {
        "request": request,
        "settings": settings,
        "page": page,
        "content": content
    })

@app.get("/team", response_class=HTMLResponse)
async def team(request: Request, db: Session = Depends(get_db)):
    settings = get_settings_dict(db)
    page, content_items = get_page_content(db, "Team")

    content = {
        'header': {},
        'team_members': []
    }

    for item in content_items:
        if item.content_type == 'page_header':
            content['header'] = item
        elif item.content_type == 'team_member':
            content['team_members'].append(item)

    return templates.TemplateResponse("team.html", {
        "request": request,
        "settings": settings,
        "page": page,
        "content": content
    })

@app.get("/testimonials", response_class=HTMLResponse)
async def testimonials(request: Request, db: Session = Depends(get_db)):
    settings = get_settings_dict(db)
    page, content_items = get_page_content(db, "Testimonials")

    content = {
        'header': {},
        'testimonials': []
    }

    for item in content_items:
        if item.content_type == 'page_header':
            content['header'] = item
        elif item.content_type == 'testimonial':
            content['testimonials'].append(item)

    return templates.TemplateResponse("testimonials.html", {
        "request": request,
        "settings": settings,
        "page": page,
        "content": content
    })

# --- Admin Panel Routes ---

@app.get("/admin", response_class=HTMLResponse)
async def admin_dashboard(request: Request, user: User = Depends(get_admin_user), db: Session = Depends(get_db)):
    pages_count = db.query(Page).count()
    content_count = db.query(ContentItem).count()
    settings_count = db.query(Setting).count()

    return templates.TemplateResponse("admin/dashboard.html", {
        "request": request,
        "user": user,
        "stats": {
            "pages": pages_count,
            "content": content_count,
            "settings": settings_count
        }
    })

@app.get("/admin/pages", response_class=HTMLResponse)
async def admin_pages(request: Request, user: User = Depends(get_admin_user), db: Session = Depends(get_db)):
    pages = db.query(Page).all()
    return templates.TemplateResponse("admin/pages.html", {
        "request": request,
        "user": user,
        "pages": pages
    })

@app.get("/admin/pages/{page_id}/edit", response_class=HTMLResponse)
async def admin_edit_page(request: Request, page_id: int, user: User = Depends(get_admin_user), db: Session = Depends(get_db)):
    page = db.query(Page).filter(Page.id == page_id).first()
    if not page:
        raise HTTPException(status_code=404, detail="Page not found")

    content_items = db.query(ContentItem).filter(
        ContentItem.page_id == page_id
    ).order_by(ContentItem.position).all()

    return templates.TemplateResponse("admin/edit_page.html", {
        "request": request,
        "user": user,
        "page": page,
        "content_items": content_items
    })

@app.get("/admin/settings", response_class=HTMLResponse)
async def admin_settings(request: Request, user: User = Depends(get_admin_user), db: Session = Depends(get_db)):
    settings = db.query(Setting).all()
    return templates.TemplateResponse("admin/settings.html", {
        "request": request,
        "user": user,
        "settings": settings
    })

# --- API Routes ---

# Pages API
@app.get("/api/pages")
def read_pages(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    pages = db.query(Page).offset(skip).limit(limit).all()
    return pages

@app.get("/api/pages/{page_id}")
def read_page(page_id: int, db: Session = Depends(get_db)):
    page = db.query(Page).filter(Page.id == page_id).first()
    if not page:
        raise HTTPException(status_code=404, detail="Page not found")
    return page

@app.post("/api/pages", dependencies=[Depends(get_admin_user)])
def create_page(page: PageCreate, user: User = Depends(get_admin_user), db: Session = Depends(get_db)):
    db_page = Page(name=page.name, added_by=user.id)
    db.add(db_page)
    db.commit()
    db.refresh(db_page)
    return db_page

@app.put("/api/pages/{page_id}", dependencies=[Depends(get_admin_user)])
def update_page(page_id: int, page: PageUpdate, user: User = Depends(get_admin_user), db: Session = Depends(get_db)):
    db_page = db.query(Page).filter(Page.id == page_id).first()
    if not db_page:
        raise HTTPException(status_code=404, detail="Page not found")

    if page.name:
        db_page.name = page.name
    db_page.modified_by = user.id
    db_page.modified_at = datetime.utcnow()

    db.commit()
    db.refresh(db_page)
    return db_page

@app.delete("/api/pages/{page_id}", dependencies=[Depends(get_admin_user)])
def delete_page(page_id: int, db: Session = Depends(get_db)):
    db_page = db.query(Page).filter(Page.id == page_id).first()
    if not db_page:
        raise HTTPException(status_code=404, detail="Page not found")
    db.delete(db_page)
    db.commit()
    return {"message": "Page deleted"}

# Content Items API
@app.get("/api/content")
def read_content(page_id: Optional[int] = None, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    query = db.query(ContentItem)
    if page_id:
        query = query.filter(ContentItem.page_id == page_id)
    content = query.order_by(ContentItem.position).offset(skip).limit(limit).all()
    return content

@app.get("/api/content/{content_id}")
def read_content_item(content_id: int, db: Session = Depends(get_db)):
    content = db.query(ContentItem).filter(ContentItem.id == content_id).first()
    if not content:
        raise HTTPException(status_code=404, detail="Content not found")
    return content

@app.post("/api/content", dependencies=[Depends(get_admin_user)])
def create_content(content: ContentItemCreate, user: User = Depends(get_admin_user), db: Session = Depends(get_db)):
    db_content = ContentItem(
        page_id=content.page_id,
        position=content.position,
        title=content.title,
        content=content.content,
        content_type=content.content_type,
        added_by=user.id
    )
    db.add(db_content)
    db.commit()
    db.refresh(db_content)
    return db_content

@app.put("/api/content/{content_id}", dependencies=[Depends(get_admin_user)])
def update_content(content_id: int, content: ContentItemUpdate, user: User = Depends(get_admin_user), db: Session = Depends(get_db)):
    db_content = db.query(ContentItem).filter(ContentItem.id == content_id).first()
    if not db_content:
        raise HTTPException(status_code=404, detail="Content not found")

    if content.position is not None:
        db_content.position = content.position
    if content.title is not None:
        db_content.title = content.title
    if content.content is not None:
        db_content.content = content.content
    if content.content_type is not None:
        db_content.content_type = content.content_type

    db_content.modified_by = user.id
    db_content.modified_at = datetime.utcnow()

    db.commit()
    db.refresh(db_content)
    return db_content

@app.delete("/api/content/{content_id}", dependencies=[Depends(get_admin_user)])
def delete_content(content_id: int, db: Session = Depends(get_db)):
    db_content = db.query(ContentItem).filter(ContentItem.id == content_id).first()
    if not db_content:
        raise HTTPException(status_code=404, detail="Content not found")
    db.delete(db_content)
    db.commit()
    return {"message": "Content deleted"}

# Settings API
@app.get("/api/settings")
def read_settings(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    settings = db.query(Setting).offset(skip).limit(limit).all()
    return settings

@app.get("/api/settings/{setting_id}")
def read_setting(setting_id: int, db: Session = Depends(get_db)):
    setting = db.query(Setting).filter(Setting.id == setting_id).first()
    if not setting:
        raise HTTPException(status_code=404, detail="Setting not found")
    return setting

@app.post("/api/settings", dependencies=[Depends(get_admin_user)])
def create_setting(setting: SettingCreate, user: User = Depends(get_admin_user), db: Session = Depends(get_db)):
    db_setting = Setting(
        reference_key=setting.reference_key,
        value=setting.value,
        added_by=user.id
    )
    db.add(db_setting)
    db.commit()
    db.refresh(db_setting)
    return db_setting

@app.put("/api/settings/{setting_id}", dependencies=[Depends(get_admin_user)])
def update_setting(setting_id: int, setting: SettingUpdate, user: User = Depends(get_admin_user), db: Session = Depends(get_db)):
    db_setting = db.query(Setting).filter(Setting.id == setting_id).first()
    if not db_setting:
        raise HTTPException(status_code=404, detail="Setting not found")

    if setting.value is not None:
        db_setting.value = setting.value
    db_setting.modified_by = user.id
    db_setting.modified_at = datetime.utcnow()

    db.commit()
    db.refresh(db_setting)
    return db_setting

@app.delete("/api/settings/{setting_id}", dependencies=[Depends(get_admin_user)])
def delete_setting(setting_id: int, db: Session = Depends(get_db)):
    db_setting = db.query(Setting).filter(Setting.id == setting_id).first()
    if not db_setting:
        raise HTTPException(status_code=404, detail="Setting not found")
    db.delete(db_setting)
    db.commit()
    return {"message": "Setting deleted"}
