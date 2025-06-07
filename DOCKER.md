# Docker Setup for Grocery API

This document provides instructions for running the Grocery API using Docker and Docker Compose.

## Prerequisites

- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)

## Getting Started

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd grocery_api
   ```

2. Create an environment file:
   ```bash
   cp .env.docker .env
   ```
   Then edit the `.env` file to set your desired configuration.

3. Run the setup script:
   ```bash
   ./docker/setup.sh
   ```

   Or manually build and start the services:
   ```bash
   docker-compose up -d --build
   ```

4. Monitor the logs:
   ```bash
   docker-compose logs -f
   ```

5. Access the application:
   - API: http://localhost:8000/
   - Admin interface: http://localhost:8000/admin/
   - API Documentation: http://localhost:8000/api/schema/swagger-ui/

## Configuration

The application uses environment variables for configuration. Key variables include:

- `DEBUG`: Set to "True" for development, "False" for production
- `SECRET_KEY`: Django secret key
- `ALLOWED_HOSTS`: Comma-separated list of allowed hosts
- `DATABASE_URL`: PostgreSQL connection URL (default: postgres://grocery_user:your_password@db:5432/grocery_api)
- `POSTGRES_DB`: PostgreSQL database name (default: grocery_api)
- `POSTGRES_USER`: PostgreSQL username (default: grocery_user)
- `POSTGRES_PASSWORD`: PostgreSQL password (default: your_password)
- `CELERY_BROKER_URL`: Redis URL for Celery (default: redis://redis:6379/0)
- `CELERY_RESULT_BACKEND`: Redis URL for Celery results (default: redis://redis:6379/0)

> **Note**: The Redis service is configured to use port 6380 on the host machine to avoid conflicts with any local Redis installations, but inside the Docker network, containers still communicate with Redis on the standard port 6379.

For a complete list of configuration options, see the `.env.docker` file.

## Services

The Docker setup includes the following services:

- **db**: PostgreSQL database (accessible at localhost:5432)
  - Database name: grocery_api
  - Username: grocery_user
  - Password: your_password
- **redis**: Redis for caching and Celery message broker (accessible at localhost:6380)
- **web**: Django web application (accessible at localhost:8000)
- **celery**: Celery worker for asynchronous tasks

## Development Workflow

### Running commands

You can run Django management commands inside the container:

```bash
docker-compose exec web python src/manage.py <command>
```

For example, to create a superuser:

```bash
docker-compose exec web python src/manage.py createsuperuser
```

### Making migrations

```bash
docker-compose exec web python src/manage.py makemigrations
docker-compose exec web python src/manage.py migrate
```

### Running tests

```bash
docker-compose exec web pytest
```

## Stopping the Services

To stop all services:

```bash
docker-compose down
```

To stop and remove volumes (this will delete all data):

```bash
docker-compose down -v
```

## Production Deployment

For production, make sure to:

1. Update the `.env` file with secure credentials
2. Set `DEBUG=False`
3. Set appropriate `ALLOWED_HOSTS`
4. Use a proper secret key
5. Enable HTTPS

For more secure deployments, consider using Docker Swarm or Kubernetes.
