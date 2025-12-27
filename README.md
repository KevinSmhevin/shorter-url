# ShortURL - URL Shortening Service

A full-stack URL shortening service with analytics, built with FastAPI (Python) and React (Vite).

## Features

- 🔗 **URL Shortening**: Create short, memorable links
- 📊 **Analytics**: Track clicks, referrers, and engagement metrics
- 🎨 **Modern UI**: Clean, responsive design with blue/gray/white theme
- 🔒 **Secure**: Input validation, URL validation, and security best practices
- ⚡ **Fast**: Built with modern, performant technologies
- 📱 **Responsive**: Works on all devices

## Tech Stack

### Backend
- **FastAPI**: Modern Python web framework
- **SQLAlchemy**: ORM for database operations
- **SQLite**: Local development database
- **PostgreSQL**: Production database support
- **Poetry**: Dependency management
- **Pydantic**: Data validation

### Frontend
- **React 18**: UI library
- **Vite**: Build tool and dev server
- **React Router**: Client-side routing
- **Tailwind CSS**: Utility-first styling
- **Axios**: HTTP client

## Project Structure

```
shorturl/
├── backend/          # FastAPI backend
│   ├── app/
│   │   ├── api/      # API routes
│   │   ├── core/     # Core utilities
│   │   ├── models/   # Database models
│   │   ├── repositories/  # Data access layer
│   │   ├── schemas/  # Pydantic schemas
│   │   ├── services/ # Business logic
│   │   └── main.py   # Application entry point
│   └── pyproject.toml
├── frontend/         # React frontend
│   ├── src/
│   │   ├── components/  # React components
│   │   ├── contexts/    # React Context
│   │   ├── pages/       # Page components
│   │   └── services/    # API service layer
│   └── package.json
└── README.md
```

## Quick Start

### Prerequisites

- Python 3.11+
- Node.js 18+
- Poetry (for backend)
- PostgreSQL (for production)

### Backend Setup

```bash
cd backend

# Install dependencies
poetry install

# Create .env file (copy from .env.example)
cp .env.example .env

# Edit .env with your configuration

# Run the server
poetry run uvicorn app.main:app --reload
```

Backend will be available at `http://localhost:8000`

### Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

Frontend will be available at `http://localhost:3000`

## API Documentation

Once the backend is running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Environment Variables

### Backend (.env)

```bash
# Application
DEBUG=true
APP_NAME=ShortURL API

# Database
DATABASE_URL=sqlite:///./shorturl.db  # Use PostgreSQL in production

# API
BASE_URL=http://localhost:8000
ALLOWED_ORIGINS=*

# Security
SECRET_KEY=your-secret-key-here
```

### Frontend (.env)

```bash
VITE_API_BASE_URL=http://localhost:8000/api/v1
```

## Production Deployment

See [PRODUCTION.md](./PRODUCTION.md) for detailed production deployment instructions.

## Robots.txt

The application includes a `robots.txt` file that:
- Prevents crawling of API endpoints (`/api/`)
- Prevents crawling of analytics pages (`/analytics/`)
- Rate limits crawlers with a 10-second crawl delay
- Allows crawling of public pages

Accessible at: `http://localhost:8000/robots.txt` or `http://localhost:3000/robots.txt`

## Security Features

- ✅ Environment variable configuration
- ✅ Input validation with Pydantic
- ✅ URL validation
- ✅ SQL injection protection (SQLAlchemy ORM)
- ✅ CORS configuration
- ✅ No secrets in code
- ✅ Error handling without information leakage

## Development

### Backend

```bash
cd backend
poetry shell
python -m app.main
```

### Frontend

```bash
cd frontend
npm run dev
```

### Building for Production

**Backend:**
```bash
cd backend
poetry install --no-dev
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker
```

**Frontend:**
```bash
cd frontend
npm run build
# Serve the dist/ directory
```

## License

MIT

## Contributing

This is a portfolio project. Feel free to fork and modify for your own use!



