# CarServ CMS - Content Management System

A complete, production-ready Content Management System built with FastAPI, PostgreSQL, and Jinja2 templates. This CMS features a car repair service website (CarServ) with a powerful admin panel (DarkPan theme) for easy content management.

## Features

### Frontend (Client Website)
- **Dynamic Pages**: Home, About, Services, Contact, Team, Testimonials
- **Database-Driven Content**: All content is stored in PostgreSQL and rendered dynamically
- **Responsive Design**: Bootstrap 5 with custom CarServ theme
- **Modern UI**: Smooth animations, carousels, and interactive elements

### Admin Panel
- **Dashboard**: Overview of pages, content items, and settings
- **Page Management**: Create, edit, rename, and delete pages
- **Content Editor**: Easy-to-use interface for editing page content
  - Support for multiple content types (carousel, features, services, team members, etc.)
  - Inline editing with modals
  - Position ordering
- **Settings Management**: Edit site-wide settings (contact info, social media, statistics)
- **User-Friendly**: No technical knowledge required for content editing

### Backend (API)
- **FastAPI**: Modern, fast Python web framework
- **RESTful APIs**: Full CRUD operations for pages, content, and settings
- **Authentication**: HTTP Basic Auth with bcrypt password hashing
- **PostgreSQL**: Robust relational database
- **SQLAlchemy ORM**: Easy database operations

## Project Structure

```
CarServCMS/
├── app/
│   ├── src/
│   │   ├── main.py                 # FastAPI application
│   │   ├── front/                  # Static files (CSS, JS, images)
│   │   │   ├── carserv-1.0.0/     # CarServ frontend theme
│   │   │   └── darkpan-1.0.0/     # DarkPan admin theme
│   │   └── templates/              # Jinja2 templates
│   │       ├── base.html           # Base template for frontend
│   │       ├── index.html          # Home page
│   │       ├── about.html
│   │       ├── services.html
│   │       ├── contact.html
│   │       ├── team.html
│   │       ├── testimonials.html
│   │       └── admin/              # Admin panel templates
│   │           ├── base.html
│   │           ├── dashboard.html
│   │           ├── pages.html
│   │           ├── edit_page.html
│   │           └── settings.html
│   ├── Dockerfile
│   └── requirements.txt
├── db/
│   └── init.sql                    # Database initialization with seed data
├── docker-compose.yml
└── README.md
```

## Database Schema

### Tables
1. **users** - User accounts with roles (admin, editor, viewer)
2. **pages** - Website pages
3. **content_items** - Content blocks for pages
4. **settings** - Site-wide configuration
5. **translations** - Multi-language support (future)

### Content Types
- `carousel` - Hero carousel items
- `feature` - Service features
- `service` - Detailed service descriptions
- `team_member` - Team member profiles
- `testimonial` - Customer testimonials
- `about` - About section content
- `about_point` - About section bullet points
- `page_header` - Page header content
- `contact_intro` - Contact page introduction

## Setup Instructions

### Prerequisites
- Docker Desktop installed and running
- Docker Compose

### Installation

1. **Start Docker Desktop** (if not already running)

2. **Navigate to project directory**:
   ```bash
   cd C:\Tech\CarServCMS
   ```

3. **Build and start containers**:
   ```bash
   docker-compose up -d --build
   ```

4. **Wait for services to start** (about 30-60 seconds)

5. **Access the application**:
   - **Frontend**: http://localhost:8000
   - **Admin Panel**: http://localhost:8000/admin
   - **API Documentation**: http://localhost:8000/docs
   - **PgAdmin**: http://localhost:5050/pgadmin

### Default Credentials

**Admin User**:
- Username: `admin`
- Password: `admin`

**PgAdmin**:
- Email: `admin@admin.com`
- Password: `admin`

**Database**:
- Host: `postgres`
- Database: `carserv`
- User: `user`
- Password: `password`

## Usage Guide

### For Administrators

#### Accessing Admin Panel
1. Go to http://localhost:8000/admin
2. Enter username: `admin`, password: `admin`
3. You'll see the dashboard with statistics

#### Managing Pages
1. Click "Pages" in the sidebar
2. Click "Edit Content" next to any page
3. Add, edit, or delete content items
4. Changes are saved immediately to the database

#### Editing Content
- **Title**: Short heading for the content item
- **Content**: Main text or data (use `||` as separator for complex types)
- **Position**: Order in which items appear (lower numbers first)
- **Type**: Select appropriate content type

#### Content Type Examples

**Service** (format: `subtitle||description||point1||point2||point3||image`):
```
15 Years Of Experience||Professional car servicing||Quality Parts||Expert Team||Fast Service||img/service-1.jpg
```

**Team Member** (format: `designation||image||facebook||twitter||instagram`):
```
Master Technician||img/team-1.jpg||https://facebook.com||https://twitter.com||https://instagram.com
```

**Testimonial** (format: `profession||review||image`):
```
Business Owner||Great service! Highly recommended.||img/testimonial-1.jpg
```

#### Managing Settings
1. Click "Settings" in the sidebar
2. Click "Edit" next to any setting
3. Update the value
4. Changes reflect immediately on the website

### For Developers

#### API Endpoints

**Pages**:
- `GET /api/pages` - List all pages
- `GET /api/pages/{id}` - Get specific page
- `POST /api/pages` - Create new page
- `PUT /api/pages/{id}` - Update page
- `DELETE /api/pages/{id}` - Delete page

**Content**:
- `GET /api/content?page_id={id}` - Get content for a page
- `GET /api/content/{id}` - Get specific content item
- `POST /api/content` - Create content item
- `PUT /api/content/{id}` - Update content item
- `DELETE /api/content/{id}` - Delete content item

**Settings**:
- `GET /api/settings` - List all settings
- `GET /api/settings/{id}` - Get specific setting
- `POST /api/settings` - Create setting
- `PUT /api/settings/{id}` - Update setting
- `DELETE /api/settings/{id}` - Delete setting

#### Authentication
All API endpoints require HTTP Basic Authentication:
```python
import requests
from requests.auth import HTTPBasicAuth

response = requests.get(
    'http://localhost:8000/api/pages',
    auth=HTTPBasicAuth('admin', 'admin')
)
```

#### Adding New Pages
```python
response = requests.post(
    'http://localhost:8000/api/pages',
    auth=HTTPBasicAuth('admin', 'admin'),
    json={'name': 'New Page'}
)
```

#### Adding Content
```python
response = requests.post(
    'http://localhost:8000/api/content',
    auth=HTTPBasicAuth('admin', 'admin'),
    json={
        'page_id': 1,
        'position': 1,
        'title': 'Welcome',
        'content': 'Welcome to our website',
        'content_type': 'text'
    }
)
```

## Customization

### Adding New Content Types
1. Update `content_type` options in `admin/edit_page.html`
2. Create template logic in appropriate page template
3. Add rendering logic in `main.py` route handlers

### Styling
- Frontend styles: `app/src/front/carserv-1.0.0/carserv-1.0.0/css/style.css`
- Admin styles: `app/src/front/darkpan-1.0.0/darkpan-1.0.0/css/style.css`

### Templates
All templates use Jinja2:
- Edit `app/src/templates/*.html` for frontend pages
- Edit `app/src/templates/admin/*.html` for admin pages

## Troubleshooting

### Container Issues
```bash
# View logs
docker-compose logs -f

# Restart containers
docker-compose restart

# Rebuild from scratch
docker-compose down -v
docker-compose up -d --build
```

### Database Issues
```bash
# Access database directly
docker exec -it carservcms-postgres-1 psql -U user -d carserv

# View tables
\dt

# Query data
SELECT * FROM pages;
SELECT * FROM content_items;
SELECT * FROM settings;
```

### Port Conflicts
If port 8000 or 5432 is already in use:
1. Edit `docker-compose.yml`
2. Change port mappings (e.g., `"8001:8000"`)
3. Restart containers

## Production Deployment

### Security Recommendations
1. **Change default passwords** in `db/init.sql`
2. **Use environment variables** for sensitive data
3. **Enable HTTPS** with reverse proxy (nginx/traefik)
4. **Set up proper authentication** (JWT tokens, OAuth)
5. **Configure CORS** properly
6. **Use secrets management** (Docker secrets, Vault)

### Performance
- Enable FastAPI caching
- Use connection pooling
- Configure PostgreSQL for production
- Add CDN for static files
- Implement rate limiting

## Features to Add

- [ ] File upload for images
- [ ] Rich text editor (WYSIWYG)
- [ ] User role management
- [ ] Activity logs
- [ ] Content versioning
- [ ] Multi-language support
- [ ] SEO management
- [ ] Form submissions
- [ ] Newsletter management
- [ ] Analytics integration

## License

This project uses templates from:
- **CarServ Template**: HTML Codex (https://htmlcodex.com)
- **DarkPan Template**: HTML Codex (https://htmlcodex.com)

## Support

For issues or questions:
1. Check logs: `docker-compose logs -f`
2. Verify database: Access PgAdmin at http://localhost:5050/pgadmin
3. Check API docs: http://localhost:8000/docs

## Technologies Used

- **Backend**: FastAPI, Python 3.10+
- **Database**: PostgreSQL 15
- **ORM**: SQLAlchemy
- **Templates**: Jinja2
- **Frontend**: Bootstrap 5, jQuery
- **Authentication**: passlib, bcrypt
- **Container**: Docker, Docker Compose
- **Database Admin**: PgAdmin 4

---

**Enjoy your new CMS! 🚗✨**

