# ShortURL Backend

A FastAPI-based URL shortening service with analytics, built with best practices in mind.

## Features

- ✅ URL shortening with custom short codes
- ✅ URL expiration support
- ✅ Click analytics and tracking
- ✅ SQLite for local development, PostgreSQL for production
- ✅ RESTful API with OpenAPI documentation
- ✅ Clean architecture with separation of concerns
- ✅ Repository pattern for data access
- ✅ Service layer for business logic
- ✅ Comprehensive error handling
- ✅ Input validation and security

## Tech Stack

- **FastAPI**: Modern, fast web framework
- **SQLAlchemy**: SQL toolkit and ORM
- **Pydantic**: Data validation using Python type annotations
- **Poetry**: Dependency management
- **SQLite**: Local development database
- **PostgreSQL**: Production database

## Project Structure

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application entry point
│   ├── config.py            # Configuration management
│   ├── database.py          # Database setup and session management
│   ├── api/
│   │   ├── routes/
│   │   │   ├── urls.py      # URL shortening endpoints
│   │   │   └── analytics.py # Analytics endpoints
│   ├── models/              # SQLAlchemy models
│   │   ├── url.py
│   │   └── analytics.py
│   ├── schemas/             # Pydantic schemas
│   │   ├── url.py
│   │   └── analytics.py
│   ├── repositories/        # Data access layer
│   │   ├── url_repository.py
│   │   └── analytics_repository.py
│   ├── services/            # Business logic layer
│   │   ├── url_service.py
│   │   └── analytics_service.py
│   └── core/                # Core utilities
│       ├── exceptions.py
│       └── security.py
├── pyproject.toml           # Poetry configuration
├── .env.example             # Environment variables template
└── README.md
```

## Setup

### Prerequisites

- Python 3.11+
- Poetry

### Installation

1. Install Poetry (if not already installed):
```bash
curl -sSL https://install.python-poetry.org | python3 -
```

2. Navigate to the backend directory:
```bash
cd backend
```

3. Install dependencies:
```bash
poetry install
```

4. Copy environment variables:
```bash
cp .env.example .env
```

5. Edit `.env` file with your configuration (especially for production):
```bash
# For local development, SQLite is already configured
# For production, update DATABASE_URL to PostgreSQL:
# DATABASE_URL=postgresql://user:password@localhost:5432/shorturl
```

6. Activate the Poetry shell:
```bash
poetry shell
```

7. Run the application:
```bash
python -m app.main
```

Or using uvicorn directly:
```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

## API Documentation

Once the server is running, you can access:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## API Endpoints

### URL Shortening

- `POST /api/v1/urls/` - Create a new shortened URL
- `GET /api/v1/urls/{short_code}` - Get URL information
- `GET /api/v1/urls/` - List all URLs (paginated)
- `DELETE /api/v1/urls/{short_code}` - Deactivate a URL
- `GET /{short_code}` - Redirect to original URL (tracks analytics)

### Analytics

- `GET /api/v1/analytics/{short_code}/summary` - Get analytics summary
- `GET /api/v1/analytics/{short_code}/clicks` - Get recent clicks

## Example Usage

### Create a shortened URL

```bash
curl -X POST "http://localhost:8000/api/v1/urls/" \
  -H "Content-Type: application/json" \
  -d '{
    "original_url": "https://example.com/very/long/url",
    "expires_in_days": 30
  }'
```

### Create with custom code

```bash
curl -X POST "http://localhost:8000/api/v1/urls/" \
  -H "Content-Type: application/json" \
  -d '{
    "original_url": "https://example.com",
    "custom_code": "my-link"
  }'
```

### Get analytics

```bash
curl "http://localhost:8000/api/v1/analytics/my-link/summary"
```

## Architecture

The application follows clean architecture principles:

1. **Models**: SQLAlchemy ORM models representing database tables
2. **Schemas**: Pydantic models for request/response validation
3. **Repositories**: Data access layer abstracting database operations
4. **Services**: Business logic layer that uses repositories
5. **Routes**: API endpoints that use services and return responses

This separation ensures:
- Testability: Each layer can be tested independently
- Maintainability: Changes in one layer don't affect others
- Extensibility: Easy to add new features or change implementations

## Security Considerations

- ✅ Environment variables for sensitive configuration
- ✅ Input validation using Pydantic
- ✅ URL validation to prevent malicious URLs
- ✅ SQL injection prevention via SQLAlchemy ORM
- ✅ No secrets in code or version control
- ✅ `.gitignore` configured to exclude `.env` files

## Database Migrations

For production, consider using Alembic for database migrations:

```bash
poetry add alembic
alembic init alembic
```

## Development

### Code Formatting

```bash
poetry run black app/
poetry run ruff check app/
```

### Type Checking

```bash
poetry run mypy app/
```

## Production Deployment

1. Set `DEBUG=false` in `.env`
2. Update `DATABASE_URL` to your PostgreSQL connection string
3. Set a strong `SECRET_KEY`
4. Update `BASE_URL` to your production domain
5. Configure CORS origins appropriately
6. Use a production ASGI server like Gunicorn with Uvicorn workers:

```bash
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker
```

## License

MIT

