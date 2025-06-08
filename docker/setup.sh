#!/bin/bash
# Script to setup Docker environment for Grocery API

set -e

# Check if docker is installed
if ! command -v docker &> /dev/null; then
    echo "Docker is not installed. Please install Docker first."
    exit 1
fi

# Check if docker-compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "Creating .env file from .env.docker..."
    cp .env.docker .env
    echo "Please edit the .env file with your configuration."

    # Give the user a moment to edit the .env file
    read -p "Press Enter after you have edited the .env file (or Ctrl+C to abort)..."
else
    echo ".env file already exists."
fi

# Create necessary directories
mkdir -p src/staticfiles src/mediafiles

# Build and start the containers
echo "Building and starting Docker containers..."
docker-compose up -d --build

# Show logs
echo "Docker containers are starting. You can check the logs with:"
echo "docker-compose logs -f"

echo ""
echo "Setup complete! You can now access the API at http://localhost:8000/"
echo "Admin interface: http://localhost:8000/admin/"
echo "API Documentation: http://localhost:8000/api/schema/swagger-ui/"
echo ""
echo "To create a superuser, run:"
echo "docker-compose exec web python src/manage.py createsuperuser"
