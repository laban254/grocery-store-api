# Grocery API

A Django-based REST API for managing a grocery store with Kubernetes deployment support and CI/CD integration.

[Swagger UI](https://grocery-api-service-e31a380bc482.herokuapp.com/api/schema/swagger-ui/)


![Tests](https://github.com/laban254/grocery-store-api/actions/workflows/ci.yml/badge.svg)
![Coverage](https://img.shields.io/badge/Coverage-85%25-success)

## Features

- Authentication & Authorization with JWT
- Product Management and Categories
- Asynchronous Order Processing with Celery
- API Documentation (OpenAPI/Swagger)
- Kubernetes Deployment Support
- CI/CD Pipeline with GitHub Actions

## Tech Stack

- Django 4.2.7 + DRF 3.14
- PostgreSQL 14 + Redis 6
- Celery 5.3.6 for Background Tasks
- Docker + Kubernetes
- GitHub Actions for CI/CD

## Quick Start

### Prerequisites

- Docker and Docker Compose
- Kubernetes cluster (for deployment)
- Git

### Local Development

1. Clone and start services:
   ```bash
   git clone <repository-url>
   cd grocery_api
   docker-compose up -d
   ```

2. Run migrations and create superuser:
   ```bash
   docker-compose exec web python src/manage.py migrate
   docker-compose exec web python src/manage.py createsuperuser
   ```

### API Documentation

Access the API documentation at:
- Swagger UI: http://localhost:8000/api/schema/swagger-ui/
- ReDoc: http://localhost:8000/api/schema/redoc/


## Development

### Testing
```bash
# Run tests with coverage (with Docker)
docker-compose exec web pytest --cov

# Run tests with coverage (local development with venv)
cd src
pytest
# or from project root
pytest src --cov=src

# For more detailed coverage reports
pytest --cov-report=term-missing  # Shows missing lines
pytest --cov-report=html  # Generates HTML report
```

### Code Quality
```bash
# Install pre-commit hooks
pre-commit install

# Run manually
pre-commit run --all-files
```

### Useful Commands
```bash
# View logs
docker-compose logs -f

# Run Django commands
docker-compose exec web python src/manage.py [command]
```

### Celery Workers

When using Docker Compose, Celery workers are started automatically. However, if you need to:

```bash
# View Celery logs
docker-compose logs -f celery

# Restart Celery workers
docker-compose restart celery

# Run Celery manually (local development without Docker)
cd src
celery -A grocery_api worker -l INFO

# Monitor Celery tasks with Flower
celery -A grocery_api flower --port=5555
```

For deployment instructions, see [KUBERNETES.md](KUBERNETES.md)

## Project Structure

```
src/
├── manage.py
├── grocery_api/      # Project configuration
├── accounts/         # User management
├── products/         # Product catalog
├── orders/          # Order processing
└── core/            # Shared functionality
```

## Additional Documentation

- [Docker Setup](DOCKER.md)
- [Kubernetes Deployment](KUBERNETES.md)
- [Application Startup](STARTUP.md)

## CI/CD Pipeline

The project includes a complete CI/CD pipeline using GitHub Actions:

### Continuous Integration (CI)
- Triggered on pull requests to main, staging, and dev branches
- Runs code quality checks (Black, Flake8)
- Executes tests with coverage reporting
- Validates database migrations

### Continuous Deployment (CD)
- Triggered on pushes to production branch or manual workflow dispatch
- Builds Docker image
- Deploys to Kubernetes cluster
- Applies all necessary Kubernetes configurations
- Verifies deployment success

For more details, see the workflow files in `.github/workflows/`.

## License

MIT License

## Troubleshooting

### Common Issues

#### Docker Compose Issues
- **Port conflicts**: Check if ports 8000, 5432, or 6380 are already in use
- **Database connection errors**: Ensure the database container is running with `docker-compose ps db`
- **Permission issues**: If you encounter permission issues with mounted volumes, run `chmod -R 777` on the affected directories

#### Kubernetes Deployment Issues
- **Image pulling errors**: Ensure the image is built locally with `docker build -t grocery_api:latest .`
- **ConfigMap issues**: Verify all required ConfigMaps are applied before deploying Pods
- **Database connectivity**: Check if the database service is correctly configured and running

#### CI/CD Pipeline Issues
- **Build failures**: Check the GitHub Actions logs for specific error details
- **Deployment failures**: Verify all required secrets are properly set in your GitHub repository
- **Database migration issues**: Ensure migrations are compatible with your database version

For detailed logs, use `docker-compose logs <service>` or `kubectl logs <pod-name>`.

For more troubleshooting information, refer to [DOCKER.md](DOCKER.md) and [KUBERNETES.md](KUBERNETES.md).

### Common Issues
1. **Pod Startup Failures**
   ```bash
   kubectl describe pod <pod-name>
   kubectl logs <pod-name>
   ```

2. **Database Connection**
   - Check PostgreSQL PVC status
   - Verify secrets are properly mounted
   - See `postgres-deployment.yaml`

3. **SSH Access**
   - Verify SSH keys in GitHub secrets
   - Check VM firewall settings
   - See `setup-ssh.sh`

### Getting Help
- [Submit an Issue](../../issues)
- Check existing issues
- Review deployment logs
