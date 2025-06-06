# Grocery API

[![CI](https://github.com/<YOUR_GITHUB_USERNAME>/grocery_api/actions/workflows/ci.yml/badge.svg)](https://github.com/<YOUR_GITHUB_USERNAME>/grocery_api/actions/workflows/ci.yml)
[![codecov](https://codecov.io/gh/<YOUR_GITHUB_USERNAME>/grocery_api/branch/main/graph/badge.svg)](https://codecov.io/gh/<YOUR_GITHUB_USERNAME>/grocery_api)

A modern REST API for grocery store management built with Django and Django REST Framework.

## Overview

This API provides a complete backend solution for managing a grocery store, including user authentication, product catalog, order processing, and more. It incorporates modern practices such as JWT authentication, OpenID Connect integration, SMS notifications, and comprehensive CI/CD pipelines.

## Features

- **User Management**
  - Custom User model with JWT-based authentication
  - Social authentication (Google, OpenID Connect)
  - Role-based permissions

- **Product Catalog**
  - Hierarchical product categories using MPTT
  - Product search and filtering
  - Stock management

- **Order Processing**
  - Order creation and management
  - Order status tracking
  - Automated SMS notifications via Africa's Talking API

- **API Documentation**
  - OpenAPI schema using drf-spectacular
  - Interactive Swagger UI

## Tech Stack

### Core Technologies
- **Backend Framework:** Django 5.2
- **API Framework:** Django REST Framework 3.16
- **Authentication:** JWT (djangorestframework-simplejwt), OAuth (django-allauth)
- **Background Tasks:** Celery with Redis
- **Hierarchical Data:** django-mptt
- **SMS Notifications:** Africa's Talking API
- **Documentation:** drf-spectacular (OpenAPI)

### Development & Quality Tools
- **Testing:** pytest, pytest-cov
- **Code Quality:** black, flake8, bandit
- **CI/CD:** GitHub Actions
- **Code Coverage:** Codecov
- **Security Scanning:** Safety, Bandit

## Getting Started

### Prerequisites

- Python 3.10+
- PostgreSQL 14+
- Redis (for Celery)
- Git

### Installation

1. Clone the repository
   ```bash
   git clone <repository-url>
   cd grocery_api
   ```

2. Create and activate a virtual environment
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies
   ```bash
   pip install -r requirements.txt
   ```

4. Set up PostgreSQL database
   ```bash
   # Log into PostgreSQL
   sudo -u postgres psql

   # Create database and user (in PostgreSQL shell)
   CREATE DATABASE grocery_api;
   CREATE USER grocery_user WITH PASSWORD 'your_password';
   ALTER ROLE grocery_user SET client_encoding TO 'utf8';
   ALTER ROLE grocery_user SET default_transaction_isolation TO 'read committed';
   ALTER ROLE grocery_user SET timezone TO 'UTC';
   GRANT ALL PRIVILEGES ON DATABASE grocery_api TO grocery_user;
   \q
   ```

5. Create a `.env` file in the project root with the following variables:
   ```
   SECRET_KEY=your_secret_key
   DEBUG=True
   ALLOWED_HOSTS=localhost,127.0.0.1

   # Database configuration
   DATABASE_URL=postgres://grocery_user:your_password@localhost:5432/grocery_api
   # Or set individual database settings
   POSTGRES_DB=grocery_api
   POSTGRES_USER=grocery_user
   POSTGRES_PASSWORD=your_password
   POSTGRES_HOST=localhost
   POSTGRES_PORT=5432

   # JWT Settings
   JWT_ACCESS_TOKEN_LIFETIME_MINUTES=60
   JWT_REFRESH_TOKEN_LIFETIME_DAYS=1

   # Africa's Talking SMS API (optional)
   AFRICAS_TALKING_ENVIRONMENT=sandbox
   AFRICAS_TALKING_API_KEY=your_api_key
   AFRICAS_TALKING_USERNAME=sandbox
   AFRICAS_TALKING_SENDER_ID=your_sender_id

   # Social Auth (optional)
   OIDC_PROVIDER_ID=your_provider_id
   OIDC_PROVIDER_NAME=Your Provider
   OIDC_SERVER_URL=https://your-provider.com
   OIDC_CLIENT_ID=your_client_id
   OIDC_CLIENT_SECRET=your_client_secret

   # Google Auth (optional)
   GOOGLE_CLIENT_ID=your_google_client_id
   GOOGLE_CLIENT_SECRET=your_google_client_secret
   ```

5. Run migrations
   ```bash
   cd src
   python manage.py migrate
   ```

6. Create a superuser
   ```bash
   python manage.py createsuperuser
   ```

7. Populate the database with sample data (optional)
   ```bash
   python manage.py populate_db
   ```

8. Start the development server
   ```bash
   python manage.py runserver
   ```

9. In a separate terminal, start Celery for background tasks
   ```bash
   cd src
   celery -A grocery_api worker --loglevel=info
   ```

### API Documentation

Once the server is running, you can access the API documentation at:

- Swagger UI: http://localhost:8000/api/schema/swagger-ui/
- ReDoc: http://localhost:8000/api/schema/redoc/
- Download OpenAPI schema: http://localhost:8000/api/schema/

### Database Management

For PostgreSQL management, you can use:

- **psql** (Command line tool)
  ```bash
  psql -U grocery_user -h localhost -d grocery_api
  ```

- **pgAdmin** (GUI tool)
  1. Install pgAdmin from https://www.pgadmin.org/
  2. Connect to your server with the credentials from your `.env` file

- **Common PostgreSQL Commands**
  ```bash
  # Connect to the database
  psql -U grocery_user -d grocery_api

  # List all tables
  \dt

  # Describe a table
  \d+ table_name

  # Execute SQL query
  SELECT * FROM accounts_user LIMIT 5;

  # Exit
  \q
  ```

## Project Structure

```
src/
  ├── manage.py
  ├── grocery_api/      # Project configuration
  ├── accounts/         # User management
  ├── products/         # Product catalog
  ├── orders/           # Order processing
  └── core/             # Shared functionality
```

## Development

### Running Tests

```bash
python manage.py test
```

### Code Quality

This project uses pre-commit hooks to maintain code quality:

```bash
# Install pre-commit hooks
pre-commit install

# Run pre-commit manually on all files
pre-commit run --all-files
```

### Using Docker (Alternative Setup)

If you prefer to use Docker for development, you can use the following setup:

1. Make sure Docker and Docker Compose are installed on your system

2. Create a `docker-compose.yml` file in the project root:
   ```yaml
   version: '3.8'

   services:
     db:
       image: postgres:14
       volumes:
         - postgres_data:/var/lib/postgresql/data/
       environment:
         - POSTGRES_DB=grocery_api
         - POSTGRES_USER=grocery_user
         - POSTGRES_PASSWORD=your_password
       ports:
         - "5432:5432"

     redis:
       image: redis:7
       ports:
         - "6379:6379"

     web:
       build: .
       command: python src/manage.py runserver 0.0.0.0:8000
       volumes:
         - .:/app
       ports:
         - "8000:8000"
       environment:
         - DATABASE_URL=postgres://grocery_user:your_password@db:5432/grocery_api
         - REDIS_URL=redis://redis:6379/0
       depends_on:
         - db
         - redis

     celery:
       build: .
       command: celery -A grocery_api worker --loglevel=info
       volumes:
         - .:/app
       environment:
         - DATABASE_URL=postgres://grocery_user:your_password@db:5432/grocery_api
         - REDIS_URL=redis://redis:6379/0
       depends_on:
         - db
         - redis

   volumes:
     postgres_data:
   ```

3. Create a `Dockerfile` in the project root:
   ```Dockerfile
   FROM python:3.10-slim

   WORKDIR /app

   ENV PYTHONDONTWRITEBYTECODE 1
   ENV PYTHONUNBUFFERED 1

   RUN apt-get update && apt-get install -y --no-install-recommends \
       gcc \
       postgresql-client \
       && rm -rf /var/lib/apt/lists/*

   COPY requirements.txt /app/
   RUN pip install --no-cache-dir -r requirements.txt

   COPY . /app/

   RUN chmod +x /app/docker-entrypoint.sh
   ENTRYPOINT ["/app/docker-entrypoint.sh"]
   ```

4. Create a `docker-entrypoint.sh` file:
   ```bash
   #!/bin/bash

   # Wait for database to be ready
   echo "Waiting for PostgreSQL..."
   while ! pg_isready -h db -p 5432 -U grocery_user -d grocery_api; do
     sleep 0.1
   done
   echo "PostgreSQL is ready"

   # Apply database migrations
   echo "Applying migrations..."
   python src/manage.py migrate

   # Create superuser if not exists
   echo "Creating superuser..."
   python src/manage.py shell -c "
   from django.contrib.auth import get_user_model;
   User = get_user_model();
   if not User.objects.filter(email='admin@example.com').exists():
       User.objects.create_superuser('admin', 'admin@example.com', 'adminpassword')
   "

   # Start server
   exec "$@"
   ```

5. Start the Docker containers:
   ```bash
   docker-compose up
   ```

## API Endpoints

### Authentication

- `POST /api/auth/token/` - Obtain JWT token
- `POST /api/auth/token/refresh/` - Refresh JWT token
- `POST /api/auth/register/` - Register a new user

### Products

- `GET /api/products/` - List all products
- `GET /api/products/{id}/` - Retrieve a product
- `GET /api/categories/` - List all categories

### Orders

- `GET /api/orders/` - List user's orders
- `POST /api/orders/` - Create a new order
- `GET /api/orders/{id}/` - Retrieve an order
- `PATCH /api/orders/{id}/` - Update an order

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgements

- [Django](https://www.djangoproject.com/)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [Africa's Talking](https://africastalking.com/)

## Development Workflow & CI/CD

### Continuous Integration

This project uses GitHub Actions for continuous integration. The CI pipeline runs automatically on:
- Pull request creation
- Pull request updates
- Pull request reopening

The CI pipeline performs the following checks:
1. **Code Quality**
   - Black formatting check
   - Flake8 linting
   - Security checks with Bandit
   - Dependency vulnerability scanning with Safety

2. **Testing**
   - Runs pytest test suite
   - Generates coverage reports
   - Uploads coverage to Codecov

3. **Database Checks**
   - Runs database migrations
   - Verifies migration integrity

### Pull Request Process

1. Create a new branch from `main`
2. Make your changes
3. Run tests locally:
   ```bash
   cd src
   pytest --cov
   ```
4. Create a pull request
5. Wait for CI checks to pass
6. Request code review
7. Address review comments
8. Merge when approved

### GitHub Secrets

The following secrets need to be configured in your GitHub repository:
- `AFRICAS_TALKING_USERNAME` - Africa's Talking API username
- `AFRICAS_TALKING_API_KEY` - Africa's Talking API key
- `GOOGLE_CLIENT_ID` - Google OAuth client ID
- `GOOGLE_CLIENT_SECRET` - Google OAuth client secret
- `SECRET_KEY` - Django secret key
- `CODECOV_TOKEN` - Codecov upload token
