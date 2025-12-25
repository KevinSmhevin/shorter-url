#!/bin/bash

# Setup script for ShortURL Backend

echo "Setting up ShortURL Backend..."

# Check if Poetry is installed
if ! command -v poetry &> /dev/null; then
    echo "Poetry is not installed. Installing Poetry..."
    curl -sSL https://install.python-poetry.org | python3 -
    export PATH="$HOME/.local/bin:$PATH"
fi

# Install dependencies
echo "Installing dependencies..."
poetry install

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "Creating .env file from template..."
    cat > .env << 'EOF'
# Application Settings
APP_NAME=ShortURL API
APP_VERSION=0.1.0
DEBUG=true

# Database Configuration
# For SQLite (local development):
DATABASE_URL=sqlite:///./shorturl.db

# For PostgreSQL (production):
# DATABASE_URL=postgresql://user:password@localhost:5432/shorturl

# Database Settings
DATABASE_ECHO=false

# API Configuration
API_V1_PREFIX=/api/v1
BASE_URL=http://localhost:8000

# Security Settings
# IMPORTANT: Change this in production!
SECRET_KEY=change-this-secret-key-in-production-use-a-strong-random-key

# URL Settings
SHORT_CODE_LENGTH=8
MAX_URL_LENGTH=2048

# Rate Limiting (for future implementation)
RATE_LIMIT_ENABLED=false
RATE_LIMIT_REQUESTS=100
RATE_LIMIT_WINDOW=60
EOF
    echo ".env file created. Please update it with your configuration."
else
    echo ".env file already exists."
fi

echo ""
echo "Setup complete!"
echo ""
echo "To run the application:"
echo "  1. Activate Poetry shell: poetry shell"
echo "  2. Run the app: python -m app.main"
echo "  3. Or use uvicorn: uvicorn app.main:app --reload"
echo ""
echo "API will be available at: http://localhost:8000"
echo "API docs at: http://localhost:8000/docs"

