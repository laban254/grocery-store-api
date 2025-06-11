# Grocery API

A Django-based REST API for managing a grocery store with Kubernetes deployment support, Heroku deployment, and CI/CD integration.

![Tests](https://github.com/laban254/grocery-store-api/actions/workflows/ci.yml/badge.svg)
![Coverage](https://img.shields.io/badge/Coverage-85%25-success)

## Features

- Authentication & Authorization with JWT
- Product Management and Categories
- Asynchronous Order Processing with Celery
- API Documentation (OpenAPI/Swagger)
- Kubernetes Deployment Support
- Heroku Deployment with Docker
- CI/CD Pipeline with GitHub Actions

## Tech Stack

- Django 4.2.7 + DRF 3.14
- PostgreSQL 14 + Redis 6
- Celery 5.3.6 for Background Tasks
- Docker and Docker Compose
- Kubernetes for Production Deployment
- Heroku for Cloud Hosting

## Getting Started

### Local Development

1. Clone the repository
```bash
git clone https://github.com/laban254/grocery-store-api.git
cd grocery-store-api
```

2. Set up a virtual environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Create a `.env` file based on the example
```bash
cp .env.example .env
# Edit .env with your settings
```

5. Apply migrations
```bash
cd src
python manage.py migrate
```

6. Run the development server
```bash
python manage.py runserver
```

### Docker Development

1. Build and start the containers
```bash
docker-compose up -d
```

2. Create a superuser
```bash
docker-compose exec web python src/manage.py createsuperuser
```

## Heroku Deployment

This application is ready to be deployed to Heroku using Docker containers.

### Prerequisites

1. Heroku CLI installed
```bash
curl https://cli-assets.heroku.com/install.sh | sh
```

2. Log in to Heroku
```bash
heroku login
```

### Deployment Steps

1. Set up your Heroku app
```bash
export APP_NAME=your-grocery-api
./scripts/setup_heroku.sh
```

2. Push to Heroku
```bash
heroku git:remote -a $APP_NAME
git push heroku main
```

3. Run database migrations
```bash
heroku run python src/manage.py migrate -a $APP_NAME
```

4. Create a superuser (optional)
```bash
heroku run python src/manage.py createsuperuser -a $APP_NAME
```

5. View your application
```bash
heroku open -a $APP_NAME
```

### Scaling Workers

To enable background task processing with Celery:

```bash
heroku ps:scale worker=1 -a $APP_NAME
```

## Kubernetes Deployment

For production-grade deployment, refer to the [KUBERNETES.md](KUBERNETES.md) guide.

## API Documentation

API documentation is available at `/api/schema/swagger-ui/` when the server is running.

## Running Tests

```bash
cd src
pytest
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.
